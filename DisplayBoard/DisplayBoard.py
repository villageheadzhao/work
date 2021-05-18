# encoding: utf-8
import time
import datetime
import smbus
import os
import threading
import csv
import tkinter as tk
import RPi.GPIO as GPIO
import LogUpload as ftp
import serial
import USBCamTest1 as Camera
import PCF8591 as AD
import Current as Cur
from tkinter import messagebox

Channel1Serial = "/dev/ttyUSBB"
Channel2Serial = "/dev/ttyUSBE"
Board1Serial = "/dev/ttyUSBA"
Board2Serial = "/dev/ttyUSBF"

StartSignal = 3
KeySignal = 2
s = 1

key_result = -1
k = 0
x = 0
ch1_key_value = 0
ch2_key_value = 0

LogNameCh1=0
LogNameCh2=0

LogSheetCh1=[]
LogSheetCh2=[]

ImageName1=""
ImageName2=""

Ch1_Vcc_Data =[]
Ch1_3v3_Data =[]
Ch1_02v_Data =[]
Ch2_Vcc_Data =[]
Ch2_3v3_Data =[]
Ch2_02v_Data =[]

ch1_key_test_value = ""
ch2_key_test_value = ""
ch1_lcd_test_value = ""
ch2_lcd_test_value = ""
ch1_d2_test_value = ""
ch1_d5_test_value = ""
ch1_d6_test_value = ""
ch2_d2_test_value = ""
ch2_d5_test_value = ""
ch2_d6_test_value = ""

ch1_show = 1
ch2_show = 1

AD1Addr = 0x48
AD2Addr = 0x49
A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) ##GPIO.BCM
GPIO.setup(35,GPIO.OUT)  ## Channel1 Realy
GPIO.setup(37,GPIO.OUT)  ## Channel2 Realy

def Signal():
    # print("step2:LCD测试判定")
    global KeySignal
    if StartSignal == 1:
        KeySignal = 1
    else:
        # print("请先进行LCD测试")
        messagebox.showinfo("警告","请先进行LCD测试")


def Ch1_LCD_Confirm():
    global Ch1LCDSignal
    Ch1LCDSignal = messagebox.askquestion('注意',"通道一的LCD屏幕是否正常，无坏点")


def Ch2_LCD_Confirm():
    global Ch2LCDSignal
    Ch2LCDSignal = messagebox.askquestion('注意',"通道二的LCD屏幕是否正常，无坏点")


def Ch1_D2_Confirm():
    global Ch1D2Signal
    Ch1D2Signal = messagebox.askquestion('注意',"通道一的D2灯是否亮绿色")


def Ch1_D5_Confirm():
    global Ch1D2Signal
    Ch1D2Signal = messagebox.askquestion('注意',"通道一的D5灯是否亮黄色")


def Ch1_D6_Confirm():
    global Ch1D2Signal
    Ch1D2Signal = messagebox.askquestion('注意',"通道一的D6灯是否亮黄色")


def Ch2_D2_Confirm():
    global Ch2D2Signal
    Ch2D2Signal = messagebox.askquestion('注意',"通道二的D2灯是否亮绿色")


def Ch2_D5_Confirm():
    global Ch2D2Signal
    Ch2D2Signal = messagebox.askquestion('注意',"通道二的D5灯是否亮黄色")


def Ch2_D6_Confirm():
    global Ch2D2Signal
    Ch2D2Signal = messagebox.askquestion('注意',"通道二的D6灯是否亮黄色")


def VolTest():
    # print("step7:电流测试")
    global label_Ch1_value_VccValue
    global label_Ch1_value_3v3
    global label_Ch1_value_02v


    global label_Ch2_value_VccValue
    global label_Ch2_value_3v3
    global label_Ch2_value_02v

    for i in range(10):
        try:
            Ch1_Vcc = Cur.CurrentRead(Board1Serial)
            Ch1_Vcc_Data.append(Ch1_Vcc)
            Ch2_Vcc = Cur.CurrentRead(Board1Serial)
            Ch2_Vcc_Data.append(Ch2_Vcc)
        except:
            # print("电流值读取异常")
            label_Ch1_value_VccValue["text"] = "读取异常"
            label_Ch1_value_VccValue["bg"] = "red"
            label_Ch2_value_VccValue["text"] = "读取异常"
            label_Ch2_value_VccValue["bg"] = "red"
            time.sleep(0.1)
        try:
            Ch1_3v3 = AD.voltage(AD1Addr,A1)
            Ch1_3v3_Data.append(Ch1_3v3)
            Ch2_3v3 = AD.voltage(AD2Addr,A1)
            Ch2_3v3_Data.append(Ch2_3v3)
            time.sleep(0.1)
            Ch1_02v = AD.voltage(AD1Addr,A2)
            Ch1_02v_Data.append(Ch1_02v)
            Ch2_02v = AD.voltage(AD2Addr,A2)
            Ch2_02v_Data.append(Ch2_02v)
            time.sleep(0.1)
            # print("Ch1_Vcc",Ch1_Vcc)
            # print("Ch1_3v3",Ch1_3v3)
            # print("Ch1_02v",Ch1_02v)
            # print("Ch2_Vcc",Ch2_Vcc)
            # print("Ch2_3v3",Ch2_3v3)
            # print("Ch2_02v",Ch2_02v)
        except:
            # print("AD读取异常")
            label_Ch1_value_02v["text"] = "读取异常"
            label_Ch1_value_02v["bg"] = "red"
            label_Ch1_value_3v3["text"] = "读取异常"
            label_Ch1_value_3v3["bg"] = "red"
            label_Ch2_value_02v["text"] = "读取异常"
            label_Ch2_value_02v["bg"] = "red"
            label_Ch2_value_3v3["text"] = "读取异常"
            label_Ch2_value_3v3["bg"] = "red"


def SortData():
    # print("step8:电流值处理判断")
    global label_Ch1_value_VccValue
    global label_Ch1_value_3v3
    global label_Ch1_value_02v
    global label_Ch1_value_LED

    global label_Ch2_value_VccValue
    global label_Ch2_value_3v3
    global label_Ch2_value_02v
    global label_Ch2_value_LED

    global Ch1_Function
    global Ch2_Function

    Ch1_Vcc_Data.sort()
    Ch1_Vcc_MaxData = Ch1_Vcc_Data[9]

    Ch1_3v3_Data.sort()
    Ch1_3v3_MaxData = Ch1_3v3_Data[9]

    Ch1_02v_Data.sort()
    Ch1_02v_MaxData = Ch1_02v_Data[9]

    Ch2_Vcc_Data.sort()
    Ch2_Vcc_MaxData = Ch2_Vcc_Data[9]

    Ch2_3v3_Data.sort()
    Ch2_3v3_MaxData = Ch2_3v3_Data[9]

    Ch2_02v_Data.sort()
    Ch2_02v_MaxData = Ch2_02v_Data[9]

    # print("Ch1_Vcc_Data[9]=",Ch1_Vcc_MaxData)
    # print("Ch1_3v3_Data[9]=",Ch1_3v3_MaxData)
    # print("Ch1_02v_Data[9]=",Ch1_02v_MaxData)
    # print("Ch2_Vcc_Data[9]=",Ch2_Vcc_MaxData)
    # print("Ch2_3v3_Data[9]=",Ch2_3v3_MaxData)
    # print("Ch2_02v_Data[9]=",Ch2_02v_MaxData)

    if (Ch1_Vcc_MaxData > 0 and Ch1_Vcc_MaxData <= 220 ):
        label_Ch1_value_VccValue['text'] = "PASS"
        label_Ch1_value_VccValue['bg'] = "green"
        Ch1_Function =  "PASS"
    else:
        label_Ch1_value_VccValue['text'] = "FAIL"
        label_Ch1_value_VccValue['bg'] = "red"
        Ch1_Function =  "NG"

    if (Ch1_3v3_MaxData > 0 and Ch1_3v3_MaxData <= 20 ):
        label_Ch1_value_3v3['text'] = "PASS"
        label_Ch1_value_3v3['bg'] = "green"
        Ch1_Function =  "PASS"
    else:
        label_Ch1_value_3v3['text'] = "FAIL"
        label_Ch1_value_3v3['bg'] = "red"
        Ch1_Function =  "NG"

    if (Ch1_02v_MaxData > 0 and Ch1_02v_MaxData <= 20 ):
        label_Ch1_value_02v['text'] = "PASS"
        label_Ch1_value_02v['bg'] = "green"
        Ch1_Function =  "PASS"
    else:
        label_Ch1_value_02v['text'] = "FAIL"
        label_Ch1_value_02v['bg'] = "red"
        Ch1_Function =  "NG"

    if (Ch2_Vcc_MaxData > 0 and Ch2_Vcc_MaxData <= 220 ):
        label_Ch2_value_VccValue['text'] = "PASS"
        label_Ch2_value_VccValue['bg'] = "green"
        Ch2_Function =  "PASS"
    else:
        label_Ch2_value_VccValue['text'] = "FAIL"
        label_Ch2_value_VccValue['bg'] = "red"
        Ch2_Function =  "NG"

    if (Ch2_3v3_MaxData > 0 and Ch2_3v3_MaxData <= 20 ):
        label_Ch2_value_3v3['text'] = "PASS"
        label_Ch2_value_3v3['bg'] = "green"
        Ch2_Function =  "PASS"
    else:
        label_Ch2_value_3v3['text'] = "FAIL"
        label_Ch2_value_3v3['bg'] = "red"
        Ch2_Function =  "NG"

    if (Ch2_02v_MaxData > 0 and Ch2_02v_MaxData <= 20 ):
        label_Ch2_value_02v['text'] = "PASS"
        label_Ch2_value_02v['bg'] = "green"
        Ch2_Function =  "PASS"
    else:
        label_Ch2_value_02v['text'] = "FAIL"
        label_Ch2_value_02v['bg'] = "red"
        Ch2_Function =  "NG"

def ChkSN():
    # print("step1: Check SN...")
    sn1_check_result = 0
    sn2_check_result = 0
    sn_check_result = 0
    sn1 = entry_Ch1.get()
    sn2 = entry_Ch2.get()

    if sn1[0:3] != "JP6":
        entry_Ch1['bg'] = 'red'
        sn1_check_result=0
    else:
        sn1_check_result=1
    if sn2[0:3] != "JP6":
        entry_Ch2['bg'] = 'red'
        sn2_check_result=0
    else:
        sn2_check_result=1

    if sn1_check_result==1 and sn2_check_result==1:
        sn_check_result = 1
    else:
        sn_check_result = 0
    return sn_check_result

def LogProcess():
    global LogSheetCh1
    global LogSheetCh2

    global LogNameCh1
    global LogNameCh2
    global ch1_lcd_test_value
    global ch2_lcd_test_value
    global ch1_key_test_value
    global ch2_key_test_value
    global ch1_d2_test_value
    global ch1_d5_test_value
    global ch1_d6_test_value
    global ch2_d2_test_value
    global ch2_d5_test_value
    global ch2_d6_test_value

    global label_Ch1_value_VccValue
    global label_Ch1_value_3v3
    global label_Ch1_value_02v
    global label_Ch1_value_LED

    global label_Ch2_value_VccValue
    global label_Ch2_value_3v3
    global label_Ch2_value_02v
    global label_Ch2_value_LED

    LogSheetCh1.append(["Ch1_D2_Function:"])
    LogSheetCh1.append([ch1_d2_test_value])
    LogSheetCh1.append(["Ch1_D5_Function:"])
    LogSheetCh1.append([ch1_d5_test_value])
    LogSheetCh1.append(["Ch1_D6_Function:"])
    LogSheetCh1.append([ch1_d6_test_value])
    LogSheetCh1.append(["Ch1_LCD_Function:"])
    LogSheetCh1.append([ch1_lcd_test_value])
    LogSheetCh1.append(["Ch1_Key_Function:"])
    LogSheetCh1.append([ch1_lcd_test_value])
    LogSheetCh1.append(["Vcc:"])
    LogSheetCh1.append(Ch1_Vcc_Data)
    LogSheetCh1.append(["3v3:"])
    LogSheetCh1.append(Ch1_3v3_Data)
    LogSheetCh1.append(["02v:"])
    LogSheetCh1.append(Ch1_02v_Data)
    LogSheetCh1.append(["End time:"])
    EndTime = datetime.datetime.now()
    LogSheetCh1.append([EndTime.strftime("%Y-%m-%d %H:%M:%S")])

    writeFileObj = open("/home/pi/Desktop/test/"+LogNameCh1+'.csv','w')
    writer = csv.writer(writeFileObj)
    for row in LogSheetCh1:
        writer.writerow(row)
    writeFileObj.close()
    time.sleep(0.1)
    ftp.LogUpload(LogNameCh1)

    LogSheetCh1.append(["Ch2_D2_Function:"])
    LogSheetCh1.append([ch2_d2_test_value])
    LogSheetCh1.append(["Ch2_D5_Function:"])
    LogSheetCh1.append([ch2_d5_test_value])
    LogSheetCh1.append(["Ch2_D6_Function:"])
    LogSheetCh1.append([ch2_d6_test_value])
    LogSheetCh2.append(["Ch2_LCD_Function:"])
    LogSheetCh2.append([ch2_lcd_test_value])
    LogSheetCh2.append(["Ch2_Key_Function:"])
    LogSheetCh2.append([ch2_lcd_test_value])
    LogSheetCh2.append(["Vcc:"])
    LogSheetCh2.append(Ch2_Vcc_Data)
    LogSheetCh2.append(["3v3:"])
    LogSheetCh2.append(Ch2_3v3_Data)
    LogSheetCh2.append(["02v:"])
    LogSheetCh2.append(Ch2_02v_Data)
    LogSheetCh2.append(["End time:"])
    EndTime = datetime.datetime.now()
    LogSheetCh2.append([EndTime.strftime("%Y-%m-%d %H:%M:%S")])

    writeFileObj = open("/home/pi/Desktop/test/"+LogNameCh2+'.csv','w')
    writer = csv.writer(writeFileObj)
    for row in LogSheetCh2:
        writer.writerow(row)
    writeFileObj.close()
    time.sleep(0.1)
    ftp.LogUpload(LogNameCh2)

    ftp.LogUploadImage(ImageName1)
    ftp.LogUploadImage(ImageName2)


def EndTest():
    global StartSignal
    global KeySignal
    global s
    global ch1_lcd_test_value
    global ch2_lcd_test_value
    global ch1_key_test_value
    global ch2_key_test_value
    global ch1_d2_test_value
    global ch1_d5_test_value
    global ch1_d6_test_value
    global ch2_d2_test_value
    global ch2_d5_test_value
    global ch2_d6_test_value

    global ch1_show
    global ch2_show
    global k
    global x
    # print("step15:结束测试")

    GPIO.output(37,GPIO.LOW)
    label_Ch1_process['text'] = '测试完成'
    label_Ch1_process['bg'] = 'green'

    label_Ch2_process['text'] = '测试完成'
    label_Ch2_process['bg'] = 'green'

    StartSignal = 3
    KeySignal = 2
    s = 1
    ch1_key_test_value = ""
    ch2_key_test_value = ""
    ch1_lcd_test_value = ""
    ch2_lcd_test_value = ""
    ch1_d2_test_value = ""
    ch1_d5_test_value = ""
    ch1_d6_test_value = ""
    ch2_d2_test_value = ""
    ch2_d5_test_value = ""
    ch2_d6_test_value = ""


    ch1_show = 1
    ch2_show = 1
    k = 0
    x = 0


def ALERT():
    global StartSignal
    global KeySignal
    global s

    GPIO.output(37,GPIO.LOW)
    label_Ch1_process['text'] = '测试中断'
    label_Ch1_process['bg'] = 'red'

    label_Ch2_process['text'] = '测试中断'
    label_Ch2_process['bg'] = 'red'

    StartSignal = 3
    KeySignal = 2
    s = 1

def LCDTest(channel):
    # print("step3:LCD测试")
    try:
        ser = serial.Serial(channel,9600)
        ser.close()
        ser.open()
        ser.flushInput()
        ser.write("lcdtest\r\n".encode("utf-8"))
        time.sleep(1)

        count = ser.inWaiting()
        recv = (ser.read(count)).decode("utf-8","ignore")
        ser.close()
    except:
        print("Error LCD")
        LCDTest(channel)

def KeyTest_Write(channel):
    # print("step5:按键测试")
    # global key_result
    try:
        # time.sleep(0.5)
        ser = serial.Serial(channel,9600)
        ser.close()
        ser.open()
        ser.flushInput()
        ser.write("keytest\r\n".encode("utf-8"))
        ser.close()
    except:
        print("Error Open Ser")
        KeyTest_Write(channel)


def KeyTest_Read(channel):
    try:
        # time.sleep(0.5)
        ser = serial.Serial(channel,9600)
        ser.close()
        ser.open()
        time.sleep(5)
        count = ser.inWaiting()
        recv_key = (ser.read(count)).decode("utf-8","ignore")
        ser.close()
        key_result = recv_key.find("done")
        print("RECV", recv_key)
        # print("KKKKKKKKK", key_result)
        return key_result
    except:
        print("Error read")


def TestProcess():
    global StartSignal
    global LogSheetCh1
    global LogSheetCh2

    global LogNameCh1
    global LogNameCh2

    global s
    global KeySignal
    global k
    global Ch1_key
    global Ch2_key
    global x
    global ch1_key_value
    global ch2_key_value

    global ImageName1
    global ImageName2

    global ch1_lcd_test_value
    global ch2_lcd_test_value
    global ch1_key_test_value
    global ch2_key_test_value
    global ch1_d2_test_value
    global ch1_d5_test_value
    global ch1_d6_test_value
    global ch2_d2_test_value
    global ch2_d5_test_value
    global ch2_d6_test_value

    global label_Ch1_LCD_value
    global label_Ch1_LCD_value
    global label_Ch1_Key_value
    global label_Ch1_Key_value
    global label_Ch1_value_VccValue
    global label_Ch1_value_VccValue
    global label_Ch1_value_3v3
    global label_Ch1_value_3v3
    global label_Ch1_value_02v
    global label_Ch1_value_02v

    global label_Ch2_LCD_value
    global label_Ch2_LCD_value
    global label_Ch2_Key_value
    global label_Ch2_Key_value
    global label_Ch2_value_VccValue
    global label_Ch2_value_VccValue
    global label_Ch2_value_3v3
    global label_Ch2_value_3v3
    global label_Ch2_value_02v
    global label_Ch2_value_02v

    global label_Ch1_process
    global label_Ch1_process

    global label_Ch2_process
    global label_Ch2_process

    global ch1_show
    global ch2_show

    global k
    global x
    k = 0
    x = 0
    ch1_show = 1
    ch2_show = 1

    StartSignal = 1

    LogSheetCh1=[]
    LogSheetCh2=[]

    LogNameCh1=0
    LogNameCh2=0

    LogNameCh1 = entry_Ch1.get()
    LogSheetCh1.append(["PartNO:"])
    LogSheetCh1.append([LogNameCh1])

    LogSheetCh1.append(["Start time:"])
    StartTime = datetime.datetime.now()
    LogSheetCh1.append([StartTime.strftime("%Y-%m-%d %H:%M:%S")])

    LogNameCh2 = entry_Ch2.get()
    LogSheetCh2.append(["PartNO:"])
    LogSheetCh2.append([LogNameCh2])

    LogSheetCh2.append(["Start time:"])
    StartTime = datetime.datetime.now()
    LogSheetCh2.append([StartTime.strftime("%Y-%m-%d %H:%M:%S")])

    ImageName1 = LogNameCh1 + LogNameCh2 + "LED"
    ImageName2 = LogNameCh1 + LogNameCh2 + "KEY"

    label_Ch1_LCD_value["text"] = "？？？"
    label_Ch1_LCD_value["bg"] = "white"
    label_Ch1_Key_value["text"] = "？？？"
    label_Ch1_Key_value["bg"] = "white"
    label_Ch1_value_VccValue['text'] = "？？？"
    label_Ch1_value_VccValue['bg'] = "white"
    label_Ch1_value_3v3['text'] = "？？？"
    label_Ch1_value_3v3['bg'] = "white"
    label_Ch1_value_02v['text'] = "？？？"
    label_Ch1_value_02v['bg'] = "white"

    label_Ch2_LCD_value["text"] = "？？？"
    label_Ch2_LCD_value["bg"] = "white"
    label_Ch2_Key_value["text"] = "？？？"
    label_Ch2_Key_value["bg"] = "white"
    label_Ch2_value_VccValue['text'] = "？？？"
    label_Ch2_value_VccValue['bg'] = "white"
    label_Ch2_value_3v3['text'] = "？？？"
    label_Ch2_value_3v3['bg'] = "white"
    label_Ch2_value_02v['text'] = "？？？"
    label_Ch2_value_02v['bg'] = "white"

    label_Ch1_process['text'] = '测试中...'
    label_Ch1_process['bg'] = 'yellow'

    label_Ch2_process['text'] = '测试中...'
    label_Ch2_process['bg'] = 'yellow'

    if ChkSN() == 1:                  #step1
        # print('SN OK')

        GPIO.output(37,GPIO.HIGH)
        time.sleep(2)
        LCDTest(Channel1Serial)                     #step3
        time.sleep(2)
        LCDTest(Channel2Serial)
        #VolTest()
        #SortData()
        Ch1_D2_Confirm()
        if Ch1D2Signal == "yes":
            label_Ch1_D2_value['text'] = 'PASS'
            label_Ch1_D2_value['bg'] = 'green'
            ch1_d2_test_value = 'PASS'
        elif Ch1D2Signal == "no":
            label_Ch1_D2_value['text'] = 'NG'
            label_Ch1_D2_value['bg'] = 'green'
            ch1_d2_test_value = 'NG'

        Ch1_D5_Confirm()
        if Ch1D5Signal == "yes":
            label_Ch1_D5_value['text'] = 'PASS'
            label_Ch1_D5_value['bg'] = 'green'
            ch1_d5_test_value = 'PASS'
        elif Ch1D5Signal == "no":
            label_Ch1_D5_value['text'] = 'NG'
            label_Ch1_D5_value['bg'] = 'green'
            ch1_d5_test_value = 'NG'

        Ch1_D6_Confirm()
        if Ch1D6Signal == "yes":
            label_Ch1_D6_value['text'] = 'PASS'
            label_Ch1_D6_value['bg'] = 'green'
            ch1_d6_test_value = 'PASS'
        elif Ch1D6Signal == "no":
            label_Ch1_D6_value['text'] = 'NG'
            label_Ch1_D6_value['bg'] = 'green'
            ch1_d6_test_value = 'NG'
        Ch2_D2_Confirm()
        if Ch2D2Signal == "yes":
            label_Ch2_D2_value['text'] = 'PASS'
            label_Ch2_D2_value['bg'] = 'green'
            ch1_d2_test_value = 'PASS'
        elif Ch2D2Signal == "no":
            label_Ch2_D2_value['text'] = 'NG'
            label_Ch2_D2_value['bg'] = 'green'
            ch1_d2_test_value = 'NG'

        Ch2_D5_Confirm()
        if Ch2D5Signal == "yes":
            label_Ch2_D5_value['text'] = 'PASS'
            label_Ch2_D5_value['bg'] = 'green'
            ch1_d5_test_value = 'PASS'
        elif Ch2D5Signal == "no":
            label_Ch2_D5_value['text'] = 'NG'
            label_Ch2_D5_value['bg'] = 'green'
            ch1_d5_test_value = 'NG'

        Ch2_D6_Confirm()
        if Ch2D6Signal == "yes":
            label_Ch2_D6_value['text'] = 'PASS'
            label_Ch2_D6_value['bg'] = 'green'
            ch1_d6_test_value = 'PASS'
        elif Ch2D6Signal == "no":
            label_Ch2_D6_value['text'] = 'NG'
            label_Ch2_D6_value['bg'] = 'green'
            ch1_d6_test_value = 'NG'


        Ch1_LCD_Confirm()
        Ch2_LCD_Confirm()
        if Ch1LCDSignal == "yes":
            label_Ch1_LCD_value['text'] = 'PASS'
            label_Ch1_LCD_value['bg'] = 'green'
            ch1_lcd_test_value = "PASS"
        elif Ch1LCDSignal == "no":
            label_Ch1_LCD_value['text'] = 'NG'
            label_Ch1_LCD_value['bg'] = 'red'
            ch1_lcd_test_value = "NG"

        if Ch2LCDSignal == "yes":
            label_Ch2_LCD_value['text'] = 'PASS'
            label_Ch2_LCD_value['bg'] = 'green'
            ch2_lcd_test_value = "PASS"
        elif Ch2LCDSignal == "no":
            label_Ch2_LCD_value['text'] = 'NG'
            label_Ch2_LCD_value['bg'] = 'red'
            ch2_lcd_test_value = "NG"
        Camera.Camera(ImageName1)     #step4
        #while (s == 1):
        #    if (KeySignal == 1):
        #        s = 0
         #   else:
         #       s = 1
        GPIO.output(37,GPIO.LOW)
        time.sleep(1)
        GPIO.output(37,GPIO.HIGH)
        time.sleep(1)

        while(k == 0):
            # print("1")

            if ch1_show == 1:
                messagebox.showinfo("提示","请进行通道一的按键测试")
                KeyTest_Write(Channel1Serial)
                ch1_show = 0

            Ch1_key = KeyTest_Read(Channel1Serial)

            if Ch1_key != -1:
                label_Ch1_Key_value["text"] = "PASS"
                label_Ch1_Key_value["bg"] = "green"
                ch1_key_test_value = "PASS"
                while (x == 0):
                    time.sleep(2)

                    if ch2_show == 1:
                        messagebox.showinfo("提示","请进行通道二的按键测试")
                        KeyTest_Write(Channel2Serial)
                        ch2_show = 0

                    Ch2_key = KeyTest_Read(Channel2Serial)

                    # print("2")
                    if Ch2_key != -1:
                        label_Ch2_Key_value["text"] = "PASS"
                        label_Ch2_Key_value["bg"] = "green"
                        ch2_key_test_value = "PASS"
                        Camera.Camera(ImageName2) #step6
                        VolTest()             #step7
                        SortData()            #step8
                        # LogProcess()          #step9
                        EndTest()             #step10
                        k = -1
                        x = -1
                        break
                    else:
                        x = 0
                        ch2_key_value += 1
                        if ch2_key_value > 10:
                            Ch2_key = 1
                            label_Ch2_Key_value["text"] = "功能异常"
                            label_Ch2_Key_value["bg"] = "red"
                            ch2_key_test_value = "NG"
                            ch2_key_value = 0
                            Camera.Camera(ImageName2) #step6
                            VolTest()             #step7
                            SortData()            #step8
                            # LogProcess()          #step9
                            EndTest()             #step10
                            k = -1
                            x = -1
                            break
                        else:
                            continue
            else:
                k = 0
                ch1_key_value += 1
                # print("ch1_key_value===", ch1_key_value)
                if ch1_key_value > 10:
                    label_Ch1_Key_value["text"] = "功能异常"
                    label_Ch1_Key_value["bg"] = "red"
                    ch1_key_test_value = "NG"
                    ch1_key_value = 0
                    while (x == 0):

                        if ch2_show == 1:
                            messagebox.showinfo("提示","请进行通道二的按键测试")
                            KeyTest_Write(Channel2Serial)
                            ch2_show = 0

                        Ch2_key = KeyTest_Read(Channel2Serial)

                        if Ch2_key != -1:
                            label_Ch2_Key_value["text"] = "PASS"
                            label_Ch2_Key_value["bg"] = "green"
                            ch2_key_test_value = "PASS"
                            Camera.Camera(ImageName2) #step6
                            VolTest()             #step7
                            SortData()            #step8
                            # LogProcess()          #step9
                            EndTest()             #step10
                            k = -1
                            x = -1
                            break
                        else:
                            x = 0
                            ch2_key_value += 1
                            if ch2_key_value > 10:
                                label_Ch2_Key_value["text"] = "功能异常"
                                label_Ch2_Key_value["bg"] = "red"
                                ch2_key_test_value = "NG"
                                ch2_key_value = 0
                                Camera.Camera(ImageName2) #step6
                                VolTest()             #step7
                                SortData()            #step8
                                # LogProcess()          #step9
                                EndTest()             #step10
                                k = -1
                                x = -1
                                break
                            else:
                                continue
                else:
                    continue
    else:
        # print('SN NG')
        ALERT()
        messagebox.showinfo("警告","请输入合法的条码")

def TestStart():
    testprocess = threading.Thread(target = TestProcess)
    try:
        testprocess.start()
    except:
        print("Error: unable to start thread")

window = tk.Tk()
window.geometry("535x300")
window.title('显示板测试')

###通道1
labelFrame_Ch1 = tk.LabelFrame(window, fg = 'blue', bg = 'white', text = "通道1")
labelFrame_Ch1.grid(row=0, column = 0)

label_Ch1_title_sn = tk.Label(labelFrame_Ch1, bg = "white", text = '请输入条码：')
label_Ch1_title_sn.grid(row = 0, column = 0, sticky = 'wn')

entry_Ch1 = tk.Entry(labelFrame_Ch1)
"""entry_Ch1.bind("<Return>", TestStart)"""
entry_Ch1.grid(row = 0, column = 1)

label_Ch1_D2 = tk.Label(labelFrame_Ch1, bg="white", text="D2功能:")
label_Ch1_D2.grid(row=1, column=0, sticky="wn")

label_Ch1_D2_value = tk.Label(labelFrame_Ch1, bg="white", text="待测")
label_Ch1_D2_value.grid(row=1, column=1, sticky="wn")

label_Ch1_D5 = tk.Label(labelFrame_Ch1, bg="white", text="D5功能:")
label_Ch1_D5.grid(row=2, column=0, sticky="wn")

label_Ch1_D5_value = tk.Label(labelFrame_Ch1, bg="white", text="待测")
label_Ch1_D5_value.grid(row=2, column=1, sticky="wn")

label_Ch1_D6 = tk.Label(labelFrame_Ch1, bg="white", text="D6功能:")
label_Ch1_D6.grid(row=3, column=0, sticky="wn")

label_Ch1_D6_value = tk.Label(labelFrame_Ch1, bg="white", text="待测")
label_Ch1_D6_value.grid(row=3, column=1, sticky="wn")

label_Ch1_LCD = tk.Label(labelFrame_Ch1, bg="white", text="LCD_Test:")
label_Ch1_LCD.grid(row=4, column=0, sticky="wn")

label_Ch1_LCD_value = tk.Label(labelFrame_Ch1, bg="white", text="待测")
label_Ch1_LCD_value.grid(row=4, column=1, sticky="wn")

label_Ch1_Key = tk.Label(labelFrame_Ch1, bg="white", text="Key_Test:")
label_Ch1_Key.grid(row=5, column=0, sticky="wn")

label_Ch1_Key_value = tk.Label(labelFrame_Ch1, bg="white", text="待测")
label_Ch1_Key_value.grid(row=5, column=1, sticky="wn")

label_Ch1_title_VccValue = tk.Label(labelFrame_Ch1, bg = "white", text = 'VCC_Current(mA)：')
label_Ch1_title_VccValue.grid(row = 6, column = 0, sticky = 'wn')

label_Ch1_value_VccValue = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_VccValue.grid(row = 6, column = 1, sticky = 'wn')

label_Ch1_title_3v3 = tk.Label(labelFrame_Ch1, bg = "white", text = '3.3V_Current(mA)：')
label_Ch1_title_3v3.grid(row = 7, column = 0, sticky = 'wn')

label_Ch1_value_3v3 = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_3v3.grid(row = 7, column = 1, sticky = 'wn')

label_Ch1_title_02v = tk.Label(labelFrame_Ch1, bg = "white", text = '0.2V_Current(mA)：')
label_Ch1_title_02v.grid(row = 8, column = 0, sticky = 'wn')

label_Ch1_value_02v = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_02v.grid(row = 8, column = 1, sticky = 'wn')

#label_Ch1_title_LED = tk.Label(labelFrame_Ch1, bg = "white", text = 'LEDK(V)：')
#label_Ch1_title_LED.grid(row = 7, column = 0, sticky = 'wn')
#
#label_Ch1_value_LED = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
#label_Ch1_value_LED.grid(row = 7, column = 1, sticky = 'wn')

label_Ch1_process = tk.Label(labelFrame_Ch1,bg = "white", text = '等待测试...')
label_Ch1_process.grid(row = 9, column = 0, sticky = 'wn')

###通道2
labelFrame_Ch2 = tk.LabelFrame(window, fg = 'blue', bg = 'white', text = "通道2")
labelFrame_Ch2.grid(row=0, column = 1)

label_Ch2_title_code = tk.Label(labelFrame_Ch2, bg = "white", text = '请输入条码：')
label_Ch2_title_code.grid(row = 0, column = 0, sticky = 'wn')

entry_Ch2 = tk.Entry(labelFrame_Ch2)
"""entry_Ch1.bind("<Return>", TestStart)"""
entry_Ch2.grid(row = 0, column = 1)

label_Ch2_D2 = tk.Label(labelFrame_Ch2, bg="white", text="D2功能:")
label_Ch2_D2.grid(row=1, column=0, sticky="wn")

label_Ch2_D2_value = tk.Label(labelFrame_Ch2, bg="white", text="待测")
label_Ch2_D2_value.grid(row=1, column=1, sticky="wn")

label_Ch2_D5 = tk.Label(labelFrame_Ch2, bg="white", text="D5功能:")
label_Ch2_D5.grid(row=2, column=0, sticky="wn")

label_Ch2_D5_value = tk.Label(labelFrame_Ch2, bg="white", text="待测")
label_Ch2_D5_value.grid(row=2, column=1, sticky="wn")

label_Ch2_D6 = tk.Label(labelFrame_Ch2, bg="white", text="D6功能:")
label_Ch2_D6.grid(row=3, column=0, sticky="wn")

label_Ch2_D6_value = tk.Label(labelFrame_Ch2, bg="white", text="待测")
label_Ch2_D6_value.grid(row=3, column=1, sticky="wn")

label_Ch2_LCD = tk.Label(labelFrame_Ch2, bg="white", text="LCD_Test:")
label_Ch2_LCD.grid(row=4, column=0, sticky="wn")

label_Ch2_LCD_value = tk.Label(labelFrame_Ch2, bg="white", text="待测")
label_Ch2_LCD_value.grid(row=4, column=1, sticky="wn")

label_Ch2_Key = tk.Label(labelFrame_Ch2, bg="white", text="Key_Test:")
label_Ch2_Key.grid(row=5, column=0, sticky="wn")

label_Ch2_Key_value = tk.Label(labelFrame_Ch2, bg="white", text="待测")
label_Ch2_Key_value.grid(row=5, column=1, sticky="wn")

label_Ch2_title_VccValue = tk.Label(labelFrame_Ch2, bg = "white", text = 'VCC_Current(mA)：')
label_Ch2_title_VccValue.grid(row=6, column = 0, sticky = 'wn')

label_Ch2_value_VccValue = tk.Label(labelFrame_Ch2, bg = "white", text = '？？？')
label_Ch2_value_VccValue.grid(row=6, column = 1, sticky = 'wn')

label_Ch2_title_3v3 = tk.Label(labelFrame_Ch2, bg = "white", text = '3.3V_Current(mA)：')
label_Ch2_title_3v3.grid(row = 7, column = 0, sticky = 'wn')

label_Ch2_value_3v3 = tk.Label(labelFrame_Ch2, bg = "white", text = '？？？')
label_Ch2_value_3v3.grid(row = 7, column = 1, sticky = 'wn')

label_Ch2_title_02v = tk.Label(labelFrame_Ch2, bg = "white", text = '0.2V_Current(mA)：')
label_Ch2_title_02v.grid(row = 8, column = 0, sticky = 'wn')

label_Ch2_value_02v = tk.Label(labelFrame_Ch2, bg = "white", text = '？？？')
label_Ch2_value_02v.grid(row = 8, column = 1, sticky = 'wn')

#label_Ch2_title_LED = tk.Label(labelFrame_Ch2, bg = "white", text = 'LEDK(V)：')
#label_Ch2_title_LED.grid(row = 7, column = 0, sticky = 'wn')
#
#label_Ch2_value_LED = tk.Label(labelFrame_Ch2, bg = "white", text = '？？？')
#label_Ch2_value_LED.grid(row = 7, column = 1, sticky = 'wn')

label_Ch2_process = tk.Label(labelFrame_Ch2,bg = "white", text = '等待测试...')
label_Ch2_process.grid(row = 9, column = 0, sticky = 'wn')

button_start = tk.Button(window,width=74,height=2,text='开始测试',padx=1,pady=1,anchor='c',command=TestStart,)
button_start.grid(row = 10, column = 0,columnspan = 2, sticky = 'wn')

#button_start = tk.Button(window,width=37,height=2,text='按键测试',padx=1,pady=1,anchor='c',command=Signal,)
#button_start.grid(row = 1, column = 1, sticky = 'wn')

window.mainloop()
