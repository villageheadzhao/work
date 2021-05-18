# coding=utf-8
# encoding: utf-8
import time
import datetime
import threading
import tkinter as tk
import serial
from binascii import *
from crcmod import *
import schedule
import math
from tkinter import messagebox
import csv
import motocontrol as mc
import plant
import numpy as np
import eventlet

com = "COM11"
com1 = "COM12"

brake_button = 0

i = 0
j = 0

forwardstart_signal = 0
reversestart_signal = 0
start_signal = 1
log = []
log1 = []
sn_log = ""
brake_data = []
torque_data = []
speed_data = []
starttime_data = []
endtime_data = []
snlog_data = []

torque_value = []
speed_value_data = []
brake_value = []
set_brake_value = 0

sn_check_result = ""
torque_max_1 = 0


def chksn():
    print("step1: Check SN...")
    global sn_check_result
    sn_check_result = 0

    sn = entry_ch1_1.get()

    if sn[0:3] != "JP6":
        entry_ch1_1['bg'] = 'red'
        sn_check_result = 0
    else:
        sn_check_result = 1
    return sn_check_result


def setdata():
    # 步距角
    global step_angle_value
    global subdivision_value
    global speed_value
    step_angle = entry_ch1_1_step_angle_value.get()
    print("step_angle===", step_angle)
    if step_angle == "":
        step_angle_value = "1.8"
    else:
        step_angle_value = step_angle
    mc.setstepangle(com, step_angle_value)
    # 细分
    subdivision = entry_ch1_1_set_subdivision_value.get()
    if subdivision == "":
        subdivision_value = "8"
    else:
        subdivision_value = subdivision
    mc.setsubdivision(com, subdivision_value)
    # 转速
    speed = entry_ch1_1_set_speed_value.get()
    if speed == "":
        speed_value = "200"
    else:
        speed_value = speed
        print('speed_value', speed_value)

    if subdivision_value == "2":
        speed_value = int(speed_value) * 2
    elif subdivision_value == "4":
        speed_value = speed_value
    elif subdivision_value == "8":
        speed_value = int(speed_value)/2
    elif subdivision_value == "16":
        speed_value = int(speed_value)/4
    elif subdivision_value == "32":
        speed_value = int(speed_value)/8
    mc.setspeed(com, speed_value)


def setbrake():
    global brake_value
    global brake_button
    brake = entry_ch1_1_set_brake_value.get()
    brake_button = brake_button + 1
    if brake == "":
        brake_value = "1.0"
    else:
        brake_value = brake
    mc.setbrake(com1, brake_value)


def dataprocess():
    global log
    global log1
    global sn_log
    sn_log = entry_ch1_1.get()
    print("log===", log)
    # log.append({"测试条码:", sn_log})
    # endtime = datetime.datetime.now()
    # log.append({"EndTime:", endtime.strftime("%Y-%m-%d %H:%M:%S")})
    writefileobj = open(sn_log + '扭矩与制动器' + '.csv', 'w', newline='')
    writer = csv.writer(writefileobj)
    writer.writerow(["SN", "StartTime", "brake", "torque", "speed", "EndTime"])
    for row in log:
        writer.writerow(row)
    writefileobj.close()


'''
    writefileobj = open(sn_log + '扭矩与转速' + '.csv', 'w', newline='')
    writer = csv.writer(writefileobj)
    writer.writerow(["SN", "StartTime", "磁粉制动器值", "扭矩值", "转速", "EndTime"])
    for row in log1:
        writer.writerow(row)
    writefileobj.close()
    time.sleep(0.1)
'''


def dataanalysis():
    print("11")
    log_name = entry_ch1_1.get()
    plant.dataanalysis(log_name)


'''
def dataanalysis1():
    print("11")
    log_name = entry_ch1_1.get()
    plant.dataanalysis1(log_name)
'''


def Get_Average(list):
   sum = 0
   for item in list:
      sum += float(item)
   return float(sum/len(list))


def forwardstart():
    global forwardstart_signal
    global reversestart_signal
    global start_signal
    global log
    global log1
    global brake_data
    global torque_data
    global speed_data
    global speed_value_data
    global ch1_1_speed_value
    global ch1_1_torque_value
    global starttime_data
    global snlog_data
    global endtime_data
    global brake_button
    global torque_value
    global set_brake_value
    global speed_value
    global brake_value
    global i
    global j
    global torque_max_1
    brake_data = []
    torque_data = []
    speed_data = []
    starttime_data = []
    endtime_data = []
    snlog_data = []
    set_brake_value = 0
    chksn()

    if start_signal == 1 and sn_check_result == 1:
        start_signal = 0
        setdata()

        reversestart_signal = 0
        forward_start_commend = "01050004FF00"
        forward_start_commend_crc16 = mc.crc16add(forward_start_commend)
        mc.forwardstart(com, forward_start_commend_crc16)
        forwardstart_signal = 1

        compare_speed = float(entry_ch1_1_set_speed_value.get())
        # compare_speed = float(float(speed)/20)
        print("compare_speed***************************", compare_speed)
        k = 0
        while k < 10:
            k += 1
            brake_data = []
            torque_data = []
            speed_data = []
            starttime_data = []
            endtime_data = []
            snlog_data = []
            i = 0
            torque_max_1 = 0
            torque_value = []

            starttime = datetime.datetime.now()
            starttime_data.append(starttime.strftime("%Y-%m-%d %H:%M:%S"))
            set_brake_value = set_brake_value + 0.2
            print("set_brake_valueset_brake_valueset_brake_value", set_brake_value)
            mc.setbrake(com1, set_brake_value)
            time.sleep(0.5)
            print("-------------------------")
            while i < 10:
                    i = i + 1
                    brake_data = []
                    torque_data = []
                    speed_data = []
                    brake = set_brake_value
                    brake_data.append(brake)
                    print("制动器", brake)
                    time.sleep(0.01)
                    torque = mc.readtorque(com1)
                    torque_data.append(torque)
                    print("转矩==", torque)
                    time.sleep(0.01)
                    speed = mc.readspeed(com1)
                    speed_data.append(speed)
                    print("转速==", speed)
                    if ((speed * 20) < compare_speed and brake > 0.6) or ((speed * 20)+120 < compare_speed and brake > 0.6):
                        k = 11
                        forwardstop()
                        break
                    else:
                        continue
                    # log.append(["000", "000", brake, torque, speed, "000"])

            brake_average = set_brake_value  # round(Get_Average(brake_data), 2)
            print("brake_average====", brake_average)

            print("torque_datatorque_datatorque_data", torque_data)
            torque_max = round(max((torque_data), default=0), 3)
            print("torque_average====", torque_max)

            speed_max = round(max((speed_data), default=0), 2)
            print("speed_average====", speed_max)

            torque_value.append(torque_max)
            speed_value_data.append(speed_max)
            brake_value.append(brake_average)
            torque_max_1 = max(torque_value)
            print("torque_max_1torque_max_1torque_max_1", torque_max_1)
            speed_max_1 = entry_ch1_1_set_speed_value.get()  # max(speed_value_data)
            brake_average_1 = max(brake_value)
            sn_log = entry_ch1_1.get()
            snlog_data.append(sn_log)
            endtime = datetime.datetime.now()
            endtime_data.append(endtime.strftime("%Y-%m-%d %H:%M:%S"))
            print("brake_buttonbrake_buttonbrake_button", brake_button)
            if float(torque_max_1) > 15:
                torque_max_1 = 0
            else:
                torque_max_1 = torque_max_1
            if float(speed_max_1) > 1000:
                speed_max_1 = 0
            else:
                speed_max_1 = speed_max_1

            ch1_1_speed_value['text'] = speed_max_1
            ch1_1_torque_value['text'] = torque_max_1

            log.append([snlog_data, starttime_data, brake_average_1, torque_max_1, speed_max_1, endtime_data])
            # log.append([snlog_data, starttime_data, brake_data, torque_data, speed_data, endtime_data])
        forwardstop()
    elif sn_check_result == 1 and start_signal == 0:
        messagebox.showinfo("错误", "电机正在测试")
    elif sn_check_result == 0:
        messagebox.showinfo("错误", "请输入合法的条码")


def forwardstop():
    global reversestart_signal
    global forwardstart_signal
    global start_signal
    global j
    global i
    global set_brake_value
    global sn_check_result
    dataprocess()
    forward_stop_commend = "010500040000"
    forward_stop_commend_crc16 = mc.crc16add(forward_stop_commend)
    mc.forwardstop(com, forward_stop_commend_crc16)
    # noinspection PyUnusedLocal
    start_signal = 1
    forwardstart_signal = 0
    reversestart_signal = 0
    j = 0
    i = 0
    set_brake_value = 0
    sn_check_result = 0
    mc.setbrake(com1, set_brake_value)


'''
def reversestart():
    global reversestart_signal
    global forwardstart_signal
    global start_signal
    if start_signal == 1:
        start_signal = 0
        setdata()
        reversestart_signal = 1
        forwardstart_signal = 0
        reverse_start_commend = "01050005FF00"
        reverse_start_commend_crc16 = mc.crc16add(reverse_start_commend)
        mc.reversestart(com, reverse_start_commend_crc16)
    else:
        messagebox.showinfo("错误", "电机正在正转")


def reversestop():
    global forwardstart_signal
    global reversestart_signal
    global start_signal
    reverse_stop_commend = "010500050000"
    reverse_stop_commend_crc16 = mc.crc16add(reverse_stop_commend)
    mc.forwardstop(com, reverse_stop_commend_crc16)
    # noinspection PyUnusedLocal
    start_signal = 1
    forwardstart_signal = 0
    reversestart_signal = 0
'''


def stop():
    global forwardstart_signal
    # global reversestart_signal
    if forwardstart_signal == 1:
        forwardstop()
    else:
        messagebox.showinfo("错误", "电机未运行")


def motorun():
    mototest = threading.Thread(target=forwardstart)
    try:
        mototest.start()
    except Exception:
        print("Error: unable to start thread")


root = tk.Tk()
root.title("电机动态扭矩测试")
root["bg"] = "#C4C4C4"
width = 600
height = 400
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
# ch1_1
ch1_1_name = tk.LabelFrame(root, fg='blue', bg='#C4C4C4',)
ch1_1_name.grid(row=0, column=0)

ch1_1_sn = tk.Label(ch1_1_name, bg="#E6E6E6", text='电机条码输入：', width=15, bd=1, relief="raised", font=('宋体', '15', 'bold'))
ch1_1_sn.grid(row=0, column=0, sticky='wn', pady=0)

entry_ch1_1 = tk.Entry(ch1_1_name, font=('宋体', '15', 'bold'), width=30, bd=1)
entry_ch1_1.grid(row=0, column=1, columnspan=2, pady=0)

ch1_1_step_angle = tk.Label(ch1_1_name, bg="#E6E6E6", text='步距角：', width=15, bd=1, relief="raised",
                            font=('宋体', '15', 'bold'))
ch1_1_step_angle.grid(row=1, column=0, sticky='wn', pady=0)

entry_ch1_1_step_angle_value = tk.Entry(ch1_1_name, font=('宋体', '15', 'bold'), width=30, bd=1)
entry_ch1_1_step_angle_value.grid(row=1, column=1, columnspan=2, pady=0)

ch1_1_set_subdivision = tk.Label(ch1_1_name, bg="#E6E6E6", text='细分：', width=15, bd=1, relief="raised",
                                 font=('宋体', '15', 'bold'))
ch1_1_set_subdivision.grid(row=2, column=0, sticky='wn', pady=0)

entry_ch1_1_set_subdivision_value = tk.Entry(ch1_1_name, font=('宋体', '15', 'bold'), width=30, bd=1)
entry_ch1_1_set_subdivision_value.grid(row=2, column=1, columnspan=2, pady=0)

ch1_1_set_speed = tk.Label(ch1_1_name, bg="#E6E6E6", text='转速(RPM)：', width=15, bd=1, relief="raised",
                           font=('宋体', '15', 'bold'))
ch1_1_set_speed.grid(row=3, column=0, sticky='wn', pady=0)

entry_ch1_1_set_speed_value = tk.Entry(ch1_1_name, font=('宋体', '15', 'bold'), width=30, bd=1)
entry_ch1_1_set_speed_value.grid(row=3, column=1, columnspan=2, pady=0)

# ch1_1_set_brake = tk.Label(ch1_1_name, bg="#E6E6E6", text='磁粉制动器设置：', width=15, bd=1, relief="raised",
#                            font=('宋体', '15', 'bold'))
# ch1_1_set_brake.grid(row=4, column=0, sticky='wn', pady=0)

# entry_ch1_1_set_brake_value = tk.Entry(ch1_1_name, font=('宋体', '16', 'bold'), width=13, bd=1)
# entry_ch1_1_set_brake_value.grid(row=4, column=1, pady=0)

# ch1_1_button_brake = tk.Button(ch1_1_name, width=18, text='设定', bd=1, bg="#E6E6E6", fg="blue", anchor='c',
#                                       font=('宋体', '11', 'bold'), command=setbrake)
# ch1_1_button_brake.grid(row=4, column=2, sticky='wn', pady=0)

ch1_1_torque = tk.Label(ch1_1_name, bg="#E6E6E6", text='扭矩值(Nm)：', width=15, bd=1, relief="raised",
                           font=('宋体', '15', 'bold'))
ch1_1_torque.grid(row=5, column=0, sticky='wn', pady=0)

ch1_1_torque_value = tk.Label(ch1_1_name, bg="#E6E6E6", text='???', width=30, bd=1, relief="raised",
                           font=('宋体', '15', 'bold'))
ch1_1_torque_value.grid(row=5, column=1, sticky='wn', columnspan=2, pady=0)


ch1_1_speed = tk.Label(ch1_1_name, bg="#E6E6E6", text='转速(RPM)：', width=15, bd=1, relief="raised",
                           font=('宋体', '15', 'bold'))
ch1_1_speed.grid(row=6, column=0, sticky='wn', pady=0)

ch1_1_speed_value = tk.Label(ch1_1_name, bg="#E6E6E6", text='???', width=30, bd=1, relief="raised",
                           font=('宋体', '15', 'bold'))
ch1_1_speed_value.grid(row=6, column=1, sticky='wn', columnspan=2, pady=0)


ch1_1_button_forward_start = tk.Button(ch1_1_name, width=16, text='正向转动', bd=1, bg="#E6E6E6", fg="blue", anchor='c',
                                       font=('宋体', '13', 'bold'), command=motorun)
ch1_1_button_forward_start.grid(row=7, column=0, sticky='wn', pady=0)

# ch1_1_button_reverse_start = tk.Button(ch1_1_name, width=16, text='反向转动', bd=1, bg="#E6E6E6", fg="blue", anchor='c',
#                                       font=('宋体', '13', 'bold'), command=reversestart)
# ch1_1_button_reverse_start.grid(row=7, column=1, sticky='wn', pady=0)

ch1_1_button_save = tk.Button(ch1_1_name, width=16, text='扭矩与转速分析', bd=1, bg="#E6E6E6", fg="blue", anchor='c',
                              font=('宋体', '13', 'bold'), command=dataanalysis)
ch1_1_button_save.grid(row=7, column=1, sticky='wn', pady=0)

ch1_1_button_stop = tk.Button(ch1_1_name, width=16, text='停止', bd=1, bg="#E6E6E6", fg="blue", anchor='c',
                              font=('宋体', '13', 'bold'), command=stop)
ch1_1_button_stop.grid(row=7, column=2, sticky='wn', pady=0)

# ch1_1_button_save = tk.Button(ch1_1_name, width=16, text='扭矩与转速分析', bd=1, bg="#E6E6E6", fg="blue", anchor='c',
#                              font=('宋体', '13', 'bold'), command=dataanalysis1)
# ch1_1_button_save.grid(row=8, column=1, sticky='wn', pady=0)

root.mainloop()

