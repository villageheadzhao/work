#coding=utf-8
# encoding: utf-8

import time
import datetime
import ch341 as AD
import os
import threading
import IOExtBrd as IO
#import i2c32 as AD
#import FlashAuto_Test as Jtest
import tkinter as tk
import pylink
import logging
import serial
import re
import binascii
from collections import Counter
import tkinter.messagebox
#import confirm
import LogUpload as ftp
import csv


p = 1
cur = 1
a = 1
f = 1
e = 1
c = 1
au = 1
pa = 1
i = 1
b = 1
jp = 1
vbat = 1


power_result = -1
current_result = -1
adctest_result = -1
flashtest_result = -1
eepromtest_result = -1
clocktest_result = -1
audiotest_result = -1
powervac_result = -1
iotest_result = -1
buzzertest_result = -1
flash_result_product = -1
vbat_result = -1

yes = -1
no = -1


LogNameCh1=0
LogSheetCh1=[]


adctest_data=[]
clocktest_data=[]
iotest_data=[]
current_data = []

def ChkSN():
    print("step1: Check SN...")
    sn1_check_result = 0

    sn1 = entry_Ch1.get()
    if sn1[0:3] != "JP6":
        entry_Ch1['bg'] = 'red'
        sn1_check_result=0
    else:
        sn1_check_result=1

    return sn1_check_result


def PowerOn():
    IO.IOExtInit(0x27)
    IO.IOExtChAWrite(0x27,0xff)


def PowerOff():
    IO.IOExtInit(0x27)
    IO.IOExtChAWrite(0x27,0x00)


def PowerOffVAC():
    IO.IOExtInit(0x27)
    IO.IOExtChAWrite(0x27,0x01)

def EndTest():
    global p
    global cur
    global a
    global f
    global e
    global c
    global pa
    global i
    global b
    global au
    global jp
    global vbat

    global current_data

    global adctest_result
    global power_result
    global current_result
    global flashtest_result
    global eepromtest_result
    global clocktest_result
    global powervac_result
    global audiotest_result
    global iotest_result
    global buzzertest_result
    global flash_result_product
    global vbat_result

    p = 1
    cur = 1
    a = 1
    f = 1
    e = 1
    c = 1
    au = 1
    pa = 1
    i = 1
    b = 1
    jp = 1
    vbat = 1



    power_result = -1
    current_result = -1
    adctest_result = -1
    flashtest_result = -1
    eepromtest_result = -1
    clocktest_result = -1
    audiotest_result = -1
    powervac_result = -1
    iotest_result = -1
    buzzertest_result = -1
    flash_result_product = -1
    vbat_result = -1


    yes = -1
    no = -1


    LogNameCh1=0
    LogSheetCh1=[]


    adctest_data=[]
    clocktest_data=[]
    iotest_data=[]
    current_data = []

    IO.IOExtInit(0x27)
    IO.IOExtChAWrite(0x27,0x00)
    label_Ch1_process['text'] = '测试完成'
    label_Ch1_process['bg'] = 'green'

'''测试程序烧录'''
def jl_test():
    logging.basicConfig()
    time.sleep(1)
    jlink=pylink.JLink()
    #jlink.reset()

    jlink.open('59401308')

    SetTif=jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
    if SetTif:
        print('Connecting CPU...')
        jlink.connect('STM32F103ZE')

        jlink.reset()

        FlashReuslt=jlink.flash_file(r'D:\1\JP6_CPU_TEST.hex',0)
        if FlashReuslt==0:
            print('Flash Success')
            IO.IOExtInit(0x27)
            IO.IOExtChAWrite(0x27,0x00)
        else:
            print('Flash Failed')

    else:
        print('Connecting Failed...')
        jlink.close()
    jlink.close()

'''产品程序烧录'''
def jl_product():
    global flash_result_product
    logging.basicConfig()
    time.sleep(1)
    jlink=pylink.JLink()
    #jlink.reset()

    jlink.open('59401308')

    SetTif=jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
    if SetTif:
        print('Connecting CPU...')
        jlink.connect('STM32F103ZE')

        jlink.reset()

        FlashReuslt=jlink.flash_file(r'D:\1\JP6_CPU_TEST.hex',0)
        if FlashReuslt==0:
            flash_result_product = 1
            print('Flash Success')
        else:
            flash_result_product = -1
            print('Flash Failed')

    else:
        print('Connecting Failed...')
        jlink.close()
    jlink.close()

'''电源'''
def Power():
    global power_result
    ser = serial.Serial(port='COM5', baudrate=9600)
    ser.close()
    ser.open()
    ser.flushInput()

    # ser.write("adctest\r\r".encode("utf-8"))
    time.sleep(1)

    count = ser.inWaiting()
    print(count)
    recv_power = (ser.read(count)).decode("utf-8")
    power_result = recv_power.find("Power On")
    print("recv_power", recv_power)
    print("power_result", power_result)
    ser.close()


def PowerVAC():
    global powervac_result
    ser = serial.Serial(port='COM5', baudrate=9600)
    ser.close()
    ser.open()
    ser.flushInput()

    ser.write("audiotest\r\r".encode("utf-8"))
    time.sleep(1)

    count = ser.inWaiting()
    print(count)
    recv_powervac = (ser.read(count)).decode("utf-8")
    powervac_result = recv_powervac.find("System")
    print(recv_powervac)
    print(powervac_result)
    ser.close()


'''adctest'''
def CPU_adctest():
    global adctest_result
    global adctest_data
    ser = serial.Serial(port='COM5', baudrate=9600)
    ser.close()
    ser.open()
    ser.flushInput()
    #a = "adctest\r\n"
    #b = binascii.b2a_hex(a)
    #print(b)
    ser.write("adctest\r\r".encode("utf-8"))
    time.sleep(1)

    count = ser.inWaiting()
    print(count)
    recv_adctest = (ser.read(count)).decode("utf-8")
    adctest_data.append(recv_adctest)
    adctest_result = recv_adctest.find("PASS")
    print(recv_adctest)
    print(adctest_data)
    print(adctest_result)
    ser.close()

'''flashtest'''
def CPU_flashtest():
    global flashtest_result
    ser = serial.Serial(port='COM5', baudrate=9600)
    ser.close()
    ser.open()
    ser.flushInput()
    #c = "flashtest\r\n"
    #d = binascii.b2a_hex(c)
    #print(d)
    ser.write("flashtest\r\r".encode("utf-8"))
    time.sleep(1)

    count = ser.inWaiting()
    print(count)
    recv_flashtest = (ser.read(count)).decode("utf-8")
    flashtest_result = recv_flashtest.find("PASS")
    print(recv_flashtest)
    print(flashtest_result)
    ser.close()

'''eepromtest'''
def CPU_eepromtest():
    global eepromtest_result
    ser = serial.Serial(port='COM5', baudrate=9600)
    ser.close()
    ser.open()
    ser.flushInput()

    ser.write("eepromtest\r\r".encode("utf-8"))
    time.sleep(1)

    count = ser.inWaiting()
    print(count)
    recv_eepromtest = (ser.read(count)).decode("utf-8")
    eepromtest_result = recv_eepromtest.find("PASS")
    print(recv_eepromtest)
    print(eepromtest_result)
    ser.close()

'''clocktest'''
def CPU_clocktest():
    global clocktest_result
    global clocktest_data
    ser = serial.Serial(port='COM5', baudrate=9600)
    ser.close()
    ser.open()
    ser.flushInput()

    ser.write("clocktest\r\r".encode("utf-8"))
    time.sleep(3)

    count = ser.inWaiting()
    print(count)
    recv_clocktest = (ser.read(count)).decode("utf-8")
    clocktest_data.append(recv_clocktest)
    clocktest_result = recv_clocktest.find("PASS")

    print(recv_clocktest)
    print(clocktest_result)
    ser.close()

'''audiotest'''
def CPU_audiotest():
    global audiotest_result
    ser = serial.Serial(port='COM5', baudrate=9600)
    ser.close()
    ser.open()
    ser.flushInput()

    ser.write("audiotest\r\r".encode("utf-8"))
    time.sleep(3)

    count = ser.inWaiting()
    print(count)
    recv_audiotest = (ser.read(count)).decode("utf-8")
    audiotest_result = recv_audiotest.find("PASS")

    print(recv_audiotest)
    print(audiotest_result)
    ser.close()

'''iotest'''
def CPU_iotest():
    global iotest_result
    global iotest_data
    ser = serial.Serial(port='COM5', baudrate=9600)
    ser.close()
    ser.open()
    ser.flushInput()

    ser.write("iotest\r\r".encode("utf-8"))
    time.sleep(3)

    count = ser.inWaiting()
    print(count)
    recv_iotest = (ser.read(count)).decode("utf-8")
    iotest_data.append(recv_iotest)
    iotest_result_count = recv_iotest.count("PASS",0,len(recv_iotest))
    if (iotest_result_count == 31):
        iotest_result = 2
    else:
        iotest_result = -1
    print(recv_iotest)
    print(iotest_result)
    ser.close()

'''buzzertest'''
def CPU_buzzertest():
    global buzzertest_result
    ser = serial.Serial(port='COM5', baudrate=9600)
    ser.close()
    ser.open()
    ser.flushInput()

    ser.write("buzzertest\r\r".encode("utf-8"))
    time.sleep(3)

    count = ser.inWaiting()
    print(count)
    recv_buzzertest = (ser.read(count)).decode("utf-8")
    buzzertest_result = recv_buzzertest.find("System")
    buzzertest_result = 10
    print(recv_buzzertest)
    print(buzzertest_result)
    ser.close()

'''buzzertest_confirm'''
def CPU_buzzertest_confirm():
    global yes
    global no
    root = tk.Toplevel()
    root.minsize(300,300)
    result = tkinter.messagebox.askquestion(title = '标题',message='是否听到蜂鸣器响？')
    print(result)
    yes = result.find("yes")
    no = result.find("no")

    if (yes == 0 or yes == -1 or no == 0 or no == -1):
        root.destroy()

    #print(yes)
    #print(no)

    #btn1 = tkinter.Button(root,text = 'CPU_buzzertest_confirm',command = CPU_buzzertest_confirm)
    #btn1.pack()
    root.mainloop()


def LogProcess():
    print(u": 记录处理...")
    global adctest_result
    global power_result
    global flashtest_result
    global eepromtest_result
    global clocktest_result
    global powervac_result
    global iotest_result
    global buzzertest_result
    global vbat_result

    global adctest_data
    global clocktest_data
    global iotest_data
    global current_data

    global label_Ch1_value_power
    global label_Ch1_value_current
    global label_Ch1_value_adctest
    global label_Ch1_value_flashtest
    global label_Ch1_value_eepromtest
    global label_Ch1_value_clocktest
    global label_Ch1_value_audiotest
    global label_Ch1_value_iotest
    global label_Ch1_value_buzzertest
    global label_Ch1_value_flash_product
    global label_Ch1_value_vBat

    global LogNameCh1

    LogSheetCh1.append(["power_result:"])
    LogSheetCh1.append(label_Ch1_value_power['text'])

    LogSheetCh1.append(["12V_Current_result:"])
    LogSheetCh1.append(label_Ch1_value_current['text'])

    LogSheetCh1.append(["adctest_result"])
    LogSheetCh1.append(label_Ch1_value_adctest['text'])

    LogSheetCh1.append(["flashtest_result"])
    LogSheetCh1.append(label_Ch1_value_flashtest['text'])

    LogSheetCh1.append(["VBat_result"])
    LogSheetCh1.append(label_Ch1_value_vBat['text'])

    LogSheetCh1.append(["eepromtest_result"])
    LogSheetCh1.append(label_Ch1_value_eepromtest['text'])

    LogSheetCh1.append(["clocktest_result"])
    LogSheetCh1.append(label_Ch1_value_clocktest['text'])

    LogSheetCh1.append(["audiotest_result"])
    LogSheetCh1.append(label_Ch1_value_audiotest['text'])

    LogSheetCh1.append(["iotest_result"])
    LogSheetCh1.append(label_Ch1_value_iotest['text'])

    LogSheetCh1.append(["buzzertest_result"])
    LogSheetCh1.append(label_Ch1_value_buzzertest['text'])

    LogSheetCh1.append(["flash_product_result"])
    LogSheetCh1.append(label_Ch1_value_flash_product['text'])

    LogSheetCh1.append(["current_data"])
    LogSheetCh1.append(current_data)

    LogSheetCh1.append(["adctest_data"])
    LogSheetCh1.append(adctest_data)

    LogSheetCh1.append(["clocktest_data"])
    LogSheetCh1.append(clocktest_data)

    LogSheetCh1.append(["iotest_data"])
    LogSheetCh1.append(iotest_data)

    LogSheetCh1.append(["End time:"])
    EndTime = datetime.datetime.now()
    LogSheetCh1.append([EndTime.strftime("%Y-%m-%d %H:%M:%S")])


    writeFileObj = open(LogNameCh1+'.csv','wb')
    writer = csv.writer(writeFileObj)
    for row in LogSheetCh1:
        writer.writerow([row])
    writeFileObj.close()
    time.sleep(0.1)
    ftp.LogUpload(LogNameCh1)

    #os.remove(LogNameCh1+'.csv')


def TestProcess():
    global p
    global cur
    global a
    global f
    global e
    global c
    global pa
    global i
    global b
    global au
    global jp
    global vbat

    global current_data

    global adctest_result
    global power_result
    global current_result
    global flashtest_result
    global eepromtest_result
    global clocktest_result
    global powervac_result
    global audiotest_result
    global iotest_result
    global buzzertest_result
    global vbat_result

    global label_Ch1_value_power
    global label_Ch1_value_current
    global label_Ch1_value_adctest
    global label_Ch1_value_flashtest
    global label_Ch1_value_eepromtest
    global label_Ch1_value_clocktest
    global label_Ch1_value_audiotest
    global label_Ch1_value_iotest
    global label_Ch1_value_buzzertest
    global label_Ch1_value_flash_product
    global label_Ch1_value_vBat

    global label_Ch1_value_power_result
    global label_Ch1_value_current_result
    global label_Ch1_value_adctest_result
    global label_Ch1_value_flashtest_result
    global label_Ch1_value_eepromtest_result
    global label_Ch1_value_clocktest_result
    global label_Ch1_value_audiotest_result
    global label_Ch1_value_iotest_result
    global label_Ch1_value_buzzertest_result
    global label_Ch1_value_flash_product_result
    global label_Ch1_value_vBat_result


    global LogSheetCh1
    global LogNameCh1

    LogSheetCh1=[]
    LogNameCh1=0

    LogNameCh1 = entry_Ch1.get()
    LogSheetCh1.append(["PartNO:"])
    LogSheetCh1.append([LogNameCh1])

    LogSheetCh1.append(["Start time:"])
    StartTime = datetime.datetime.now()
    LogSheetCh1.append([StartTime.strftime("%Y-%m-%d %H:%M:%S")])
    #PowerOff()



    label_Ch1_process['text'] = '测试中...'
    label_Ch1_process['bg'] = 'yellow'

    label_Ch1_value_power['text'] = '？？？'
    label_Ch1_value_power['bg'] = 'white'

    label_Ch1_value_current['text'] = '？？？'
    label_Ch1_value_current['bg'] = 'white'

    label_Ch1_value_adctest['text'] = '？？？'
    label_Ch1_value_adctest['bg'] = 'white'

    label_Ch1_value_flashtest['text'] = '？？？'
    label_Ch1_value_flashtest['bg'] = 'white'

    label_Ch1_value_vBat['text'] = '？？？'
    label_Ch1_value_vBat['bg'] = 'white'

    label_Ch1_value_eepromtest['text'] = '？？？'
    label_Ch1_value_eepromtest['bg'] = 'white'

    label_Ch1_value_clocktest['text'] = '？？？'
    label_Ch1_value_clocktest['bg'] = 'white'

    label_Ch1_value_audiotest['text'] = '？？？'
    label_Ch1_value_audiotest['bg'] = 'white'

    label_Ch1_value_iotest['text'] = '？？？'
    label_Ch1_value_iotest['bg'] = 'white'

    label_Ch1_value_buzzertest['text'] = '？？？'
    label_Ch1_value_buzzertest['bg'] = 'white'

    label_Ch1_value_flash_product['text'] = '？？？'
    label_Ch1_value_flash_product['bg'] = 'white'

    if ChkSN() == 1:
        PowerOn()
        #PowerOff()
        time.sleep(1)
        jl_test()
        #time.sleep(1)
        PowerOn()
        '''power'''
        Power()
        while (p ==1):
            if (power_result != -1):
                label_Ch1_value_power['text'] = 'PASS'
                label_Ch1_value_power['bg'] = 'green'
                label_Ch1_value_power_result = 1
                print(u"设置power为PASS")
                power_result = 2
                p = 0
            else:
                label_Ch1_value_power['text'] = 'FAIL'
                label_Ch1_value_power['bg'] = 'red'
                label_Ch1_value_power_result = -1

                label_Ch1_value_adctest['text'] = 'FAIL'
                label_Ch1_value_adctest['bg'] = 'red'
                label_Ch1_value_adctest_result = -1

                label_Ch1_value_flashtest['text'] = 'FAIL'
                label_Ch1_value_flashtest['bg'] = 'red'
                label_Ch1_value_flashtest_result = -1

                label_Ch1_value_eepromtest['text'] = 'FAIL'
                label_Ch1_value_eepromtest['bg'] = 'red'
                label_Ch1_value_eepromtest_result = -1

                label_Ch1_value_clocktest['text'] = 'FAIL'
                label_Ch1_value_clocktest['bg'] = 'red'
                label_Ch1_value_clocktest_result = -1

                label_Ch1_value_audiotest['text'] = 'FAIL'
                label_Ch1_value_audiotest['bg'] = 'red'
                label_Ch1_value_audiotest_result = -1

                label_Ch1_value_iotest['text'] = 'FAIL'
                label_Ch1_value_iotest['bg'] = 'red'
                label_Ch1_value_iotest_result = -1

                label_Ch1_value_buzzertest['text'] = 'FAIL'
                label_Ch1_value_buzzertest['bg'] = 'red'
                label_Ch1_value_buzzertest_result = -1

                label_Ch1_value_flash_product['text'] = 'FAIL'
                label_Ch1_value_flash_product['bg'] = 'red'
                label_Ch1_value_flash_product_result = -1



                power_result = -1
               # LogProcess()
                EndTest()
                p = 0
                cur = 0
                a = 0
                f = 0
                e = 0
                c = 0
                au = 0
                pa = 0
                i = 0
                b = 0
                jp = 0

        if (power_result != -1):
            data = AD.CH341()
            voltage1 = data.read(0x48,0x40)
            voltage2 = data.read(0x48,0x40)
            voltage3 = data.read(0x48,0x40)
            time.sleep(0.5)
            voltage = data.read(0x48,0x40)
            current_data = voltage/2.56
            print("current=====",current_data)
            print("voltage",voltage)
            data.flushbuffer()

        else:
            print(u"设置power为false")

        while(cur == 1):
            if (current_data >20 and current_data <30):
                label_Ch1_value_current['text'] = 'PASS'
                label_Ch1_value_current['bg'] = 'green'
                label_Ch1_value_current_result = 1
                current_result = 2
                cur = 0
            else:
                label_Ch1_value_current['text'] = 'FAIL'
                label_Ch1_value_current['bg'] = 'red'
                label_Ch1_value_current_result = -1

                label_Ch1_value_adctest['text'] = 'FAIL'
                label_Ch1_value_adctest['bg'] = 'red'
                label_Ch1_value_adctest_result = -1

                label_Ch1_value_flashtest['text'] = 'FAIL'
                label_Ch1_value_flashtest['bg'] = 'red'
                label_Ch1_value_flashtest_result = -1

                label_Ch1_value_eepromtest['text'] = 'FAIL'
                label_Ch1_value_eepromtest['bg'] = 'red'
                label_Ch1_value_eepromtest_result = -1

                label_Ch1_value_clocktest['text'] = 'FAIL'
                label_Ch1_value_clocktest['bg'] = 'red'
                label_Ch1_value_clocktest_result = -1

                label_Ch1_value_audiotest['text'] = 'FAIL'
                label_Ch1_value_audiotest['bg'] = 'red'
                label_Ch1_value_audiotest_result = -1

                label_Ch1_value_iotest['text'] = 'FAIL'
                label_Ch1_value_iotest['bg'] = 'red'
                label_Ch1_value_iotest_result = -1

                label_Ch1_value_buzzertest['text'] = 'FAIL'
                label_Ch1_value_buzzertest['bg'] = 'red'
                label_Ch1_value_buzzertest_result = -1

                label_Ch1_value_flash_product['text'] = 'FAIL'
                label_Ch1_value_flash_product['bg'] = 'red'
                label_Ch1_value_flash_product_result = -1
                current_result = -1
               # LogProcess()
                EndTest()
                cur = 0
                a = 0
                f = 0
                e = 0
                c = 0
                au = 0
                pa = 0
                i = 0
                b = 0
                jp = 0


        '''adctest'''
        if (current_result != -1):
            CPU_adctest()
        else:
            print(u"设置power为false")

        while (a == 1):
            if (adctest_result != -1):
                label_Ch1_value_adctest['text'] = 'PASS'
                label_Ch1_value_adctest['bg'] = 'green'
                label_Ch1_value_adctest_result = 1
                print(u"设置adctest为PASS")
                adctest_result = 2
                a = 0
            else:
                label_Ch1_value_adctest['text'] = 'FAIL'
                label_Ch1_value_adctest['bg'] = 'red'
                label_Ch1_value_adctest_result = -1

                label_Ch1_value_flashtest['text'] = 'FAIL'
                label_Ch1_value_flashtest['bg'] = 'red'
                label_Ch1_value_flashtest_result = -1

                label_Ch1_value_eepromtest['text'] = 'FAIL'
                label_Ch1_value_eepromtest['bg'] = 'red'
                label_Ch1_value_eepromtest_result = -1

                label_Ch1_value_clocktest['text'] = 'FAIL'
                label_Ch1_value_clocktest['bg'] = 'red'
                label_Ch1_value_clocktest_result = -1

                label_Ch1_value_audiotest['text'] = 'FAIL'
                label_Ch1_value_audiotest['bg'] = 'red'
                label_Ch1_value_audiotest_result = -1

                label_Ch1_value_iotest['text'] = 'FAIL'
                label_Ch1_value_iotest['bg'] = 'red'
                label_Ch1_value_iotest_result = -1

                label_Ch1_value_buzzertest['text'] = 'FAIL'
                label_Ch1_value_buzzertest['bg'] = 'red'
                label_Ch1_value_buzzertest_result = -1

                label_Ch1_value_flash_product['text'] = 'FAIL'
                label_Ch1_value_flash_product['bg'] = 'red'
                label_Ch1_value_flash_product_result = -1

                adctest_result = -1
               # LogProcess()
                EndTest()
                a = 0
                f = 0
                e = 0
                c = 0
                au = 0
                pa = 0
                i = 0
                b = 0
                jp = 0

        '''flashtest'''
        if (adctest_result != -1):
            CPU_flashtest()
        else:
            print(u"设置adctest为false")

        while (f == 1):
            if (flashtest_result != -1):
                label_Ch1_value_flashtest['text'] = 'PASS'
                label_Ch1_value_flashtest['bg'] = 'green'
                label_Ch1_value_flashtest_result = 1
                print(u"设置flashtest为PASS")
                flashtest_result = 2
                f = 0
            else:
                label_Ch1_value_flashtest['text'] = 'FAIL'
                label_Ch1_value_flashtest['bg'] = 'red'
                label_Ch1_value_flashtest_result = -1

                label_Ch1_value_vBat['text'] = 'FAIL'
                label_Ch1_value_vBat['bg'] = 'red'
                label_Ch1_value_vBat_result = -1

                label_Ch1_value_eepromtest['text'] = 'FAIL'
                label_Ch1_value_eepromtest['bg'] = 'red'
                label_Ch1_value_eepromtest_result = -1

                label_Ch1_value_clocktest['text'] = 'FAIL'
                label_Ch1_value_clocktest['bg'] = 'red'
                label_Ch1_value_clocktest_result = -1

                label_Ch1_value_audiotest['text'] = 'FAIL'
                label_Ch1_value_audiotest['bg'] = 'red'
                label_Ch1_value_audiotest_result = -1

                label_Ch1_value_iotest['text'] = 'FAIL'
                label_Ch1_value_iotest['bg'] = 'red'
                label_Ch1_value_iotest_result = -1

                label_Ch1_value_buzzertest['text'] = 'FAIL'
                label_Ch1_value_buzzertest['bg'] = 'red'
                label_Ch1_value_buzzertest_result = -1

                label_Ch1_value_flash_product['text'] = 'FAIL'
                label_Ch1_value_flash_product['bg'] = 'red'
                label_Ch1_value_flash_product_result = -1

                flashtest_result = -1
               # LogProcess()
                EndTest()
                f = 0
                vbat = 0
                e = 0
                c = 0
                au = 0
                pa = 0
                i = 0
                b = 0
                jp = 0

        PowerOffVAC()
        if (flashtest_result != -1):
            flashtest_result = -1
            CPU_flashtest()
        else:
            print(u"设置flashtest为false")

        while (vbat == 1):
            if (flashtest_result != -1):
                label_Ch1_value_vBat['text'] = 'PASS'
                label_Ch1_value_vBat['bg'] = 'green'
                label_Ch1_value_vBat_result = 1
                print(u"设置Vcc_BAT为PASS")
                vbat_result = 2
                vbat = 0
            else:
                label_Ch1_value_vBat['text'] = 'FAIL'
                label_Ch1_value_vBat['bg'] = 'red'
                label_Ch1_value_vBat_result = -1

                label_Ch1_value_eepromtest['text'] = 'FAIL'
                label_Ch1_value_eepromtest['bg'] = 'red'
                label_Ch1_value_eepromtest_result = -1

                label_Ch1_value_clocktest['text'] = 'FAIL'
                label_Ch1_value_clocktest['bg'] = 'red'
                label_Ch1_value_clocktest_result = -1

                label_Ch1_value_audiotest['text'] = 'FAIL'
                label_Ch1_value_audiotest['bg'] = 'red'
                label_Ch1_value_audiotest_result = -1

                label_Ch1_value_iotest['text'] = 'FAIL'
                label_Ch1_value_iotest['bg'] = 'red'
                label_Ch1_value_iotest_result = -1

                label_Ch1_value_buzzertest['text'] = 'FAIL'
                label_Ch1_value_buzzertest['bg'] = 'red'
                label_Ch1_value_buzzertest_result = -1

                label_Ch1_value_flash_product['text'] = 'FAIL'
                label_Ch1_value_flash_product['bg'] = 'red'
                label_Ch1_value_flash_product_result = -1

                eepromtest_result = -1
               # LogProcess()
                EndTest()
                e = 0
                c = 0
                au = 0
                pa = 0
                i = 0
                b = 0
                jp = 0

        '''eepromtest'''
        if (vbat_result != -1):
            CPU_eepromtest()
        else:

            print(u"设置Vcc_BAT为false")

        while (e == 1):
            if (eepromtest_result != -1):
                label_Ch1_value_eepromtest['text'] = 'PASS'
                label_Ch1_value_eepromtest['bg'] = 'green'
                label_Ch1_value_eepromtest_result = 1
                print(u"设置eepromtest为PASS")
                eepromtest_result = 2
                e = 0
            else:
                label_Ch1_value_eepromtest['text'] = 'FAIL'
                label_Ch1_value_eepromtest['bg'] = 'red'
                label_Ch1_value_eepromtest_result = -1

                label_Ch1_value_clocktest['text'] = 'FAIL'
                label_Ch1_value_clocktest['bg'] = 'red'
                label_Ch1_value_clocktest_result = -1

                label_Ch1_value_audiotest['text'] = 'FAIL'
                label_Ch1_value_audiotest['bg'] = 'red'
                label_Ch1_value_audiotest_result = -1

                label_Ch1_value_iotest['text'] = 'FAIL'
                label_Ch1_value_iotest['bg'] = 'red'
                label_Ch1_value_iotest_result = -1

                label_Ch1_value_buzzertest['text'] = 'FAIL'
                label_Ch1_value_buzzertest['bg'] = 'red'
                label_Ch1_value_buzzertest_result = -1

                label_Ch1_value_flash_product['text'] = 'FAIL'
                label_Ch1_value_flash_product['bg'] = 'red'
                label_Ch1_value_flash_product_result = -1

                eepromtest_result = -1
               # LogProcess()
                EndTest()
                e = 0
                c = 0
                au = 0
                pa = 0
                i = 0
                b = 0
                jp = 0


        '''clocktest'''
        if (eepromtest_result != -1):
            CPU_clocktest()
        else:

            print(u"设置eepromtest为false")

        while (c == 1):
            if (clocktest_result != -1):
                label_Ch1_value_clocktest['text'] = 'PASS'
                label_Ch1_value_clocktest['bg'] = 'green'
                label_Ch1_value_clocktest_result = 1
                print(u"设置clocktest为PASS")
                clocktest_result = 2
                c = 0
            else:
                label_Ch1_value_clocktest['text'] = 'FAIL'
                label_Ch1_value_clocktest['bg'] = 'red'
                label_Ch1_value_clocktest_result = -1

                label_Ch1_value_audiotest['text'] = 'FAIL'
                label_Ch1_value_audiotest['bg'] = 'red'
                label_Ch1_value_audiotest_result = -1

                label_Ch1_value_iotest['text'] = 'FAIL'
                label_Ch1_value_iotest['bg'] = 'red'
                label_Ch1_value_iotest_result = -1

                label_Ch1_value_buzzertest['text'] = 'FAIL'
                label_Ch1_value_buzzertest['bg'] = 'red'
                label_Ch1_value_buzzertest_result = -1

                label_Ch1_value_flash_product['text'] = 'FAIL'
                label_Ch1_value_flash_product['bg'] = 'red'
                label_Ch1_value_flash_product_result = -1

                clocktest_result = -1
                #LogProcess()
                EndTest()
                c = 0
                au = 0
                pa = 0
                i = 0
                b = 0
                jp = 0

        '''audiotest'''
        if (clocktest_result != -1):
            CPU_audiotest()
        else:
            print(u"设置clocktest为false")
        time.sleep(3)
        while (au == 1):
            if (audiotest_result != -1):
                label_Ch1_value_audiotest['text'] = 'PASS'
                label_Ch1_value_audiotest['bg'] = 'green'
                label_Ch1_value_audiotest_result = 1
                print(u"设置audiotest为PASS")
                audiotest_result = 2
                au = 0
            else:
                label_Ch1_value_audiotest['text'] = 'FAIL'
                label_Ch1_value_audiotest['bg'] = 'red'
                label_Ch1_value_audiotest_result = -1

                label_Ch1_value_iotest['text'] = 'FAIL'
                label_Ch1_value_iotest['bg'] = 'red'
                label_Ch1_value_iotest_result = -1

                label_Ch1_value_buzzertest['text'] = 'FAIL'
                label_Ch1_value_buzzertest['bg'] = 'red'
                label_Ch1_value_buzzertest_result = -1

                label_Ch1_value_flash_product['text'] = 'FAIL'
                label_Ch1_value_flash_product['bg'] = 'red'
                label_Ch1_value_flash_product_result = -1

                audiotest_result = -1
                #LogProcess()
                EndTest()
                au = 0
                pa = 0
                i = 0
                b = 0
                jp = 0
        '''iotest'''
        if (audiotest_result != -1):
            CPU_iotest()
        else:
            print(u"设置audiotest为false")

        while (i == 1):
            if (iotest_result != -1):
                label_Ch1_value_iotest['text'] = 'PASS'
                label_Ch1_value_iotest['bg'] = 'green'
                label_Ch1_value_iotest_result = 1
                print(u"设置audiotest为PASS")
                iotest_result = 2
                i = 0
            else:
                label_Ch1_value_iotest['text'] = 'FAIL'
                label_Ch1_value_iotest['bg'] = 'red'
                label_Ch1_value_iotest_result = -1

                label_Ch1_value_buzzertest['text'] = 'FAIL'
                label_Ch1_value_buzzertest['bg'] = 'red'
                label_Ch1_value_buzzertest_result = -1

                label_Ch1_value_flash_product['text'] = 'FAIL'
                label_Ch1_value_flash_product['bg'] = 'red'
                label_Ch1_value_flash_product_result = -1

                iotest_result = -1
                #LogProcess()
                EndTest()
                i = 0
                b = 0
                jp = 0

        '''buzzertest'''
        print(iotest_result)
        if (iotest_result != -1):
            CPU_buzzertest()
            time.sleep(3)
        else:
            print(u"设置iotest为false")

        while (b == 1):
            if (yes != -1):
                label_Ch1_value_buzzertest['text'] = 'PASS'
                label_Ch1_value_buzzertest['bg'] = 'green'
                label_Ch1_value_buzzertest_result = 1
                print(u"设置buzzertest为PASS")
                buzzertest_result = 2
                b = 0
            else:
                label_Ch1_value_buzzertest['text'] = 'FAIL'
                label_Ch1_value_buzzertest['bg'] = 'red'
                label_Ch1_value_buzzertest_result = -1

                label_Ch1_value_flash_product['text'] = 'FAIL'
                label_Ch1_value_flash_product['bg'] = 'red'
                label_Ch1_value_flash_product_result = -1
                b = 0
                jp = 0
        time.sleep(2)
        PowerOff()
        time.sleep(1)
        while (jp == 1):
            if (label_Ch1_value_current_result == 1 and label_Ch1_value_power_result == 1 and label_Ch1_value_adctest_result == 1 and label_Ch1_value_flashtest_result == 1 and label_Ch1_value_eepromtest_result ==1 and label_Ch1_value_clocktest_result == 1 and label_Ch1_value_audiotest_result ==1 and label_Ch1_value_iotest_result ==1 and label_Ch1_value_buzzertest_result == 1):
                PowerOn()
                jl_product()
                if flash_result_product == 1:
                    label_Ch1_value_flash_product['text'] = 'PASS'
                    label_Ch1_value_flash_product['bg'] = 'green'
                else:
                    label_Ch1_value_flash_product['text'] = 'FAIL'
                    label_Ch1_value_flash_product['bg'] = 'red'
                #LogProcess()
                EndTest()
                jp = 0
            else:
                label_Ch1_value_flash_product['text'] = 'FAIL'
                label_Ch1_value_flash_product['bg'] = 'red'
                #LogProcess()
                EndTest()
                jp = 0
        #if (p == 0 or cur == 0 or a == 0 or f == 0 or e == 0 or c == 0 or au == 0 or pa == 0 or i == 1 or b ==1 or jp == 1):

        EndTest()
        LogProcess()

    else:
        label_Ch1_process['text'] = '请输入合法条码'
        label_Ch1_process['bg'] = 'red'


def TestStart():
    testprocess = threading.Thread(target = TestProcess)
    #testprocess1 = threading.Thread(target = CPU_buzzertest_confirm)
    try:
        testprocess.start()
        #time.sleep(5)
        #testprocess1.start()

    except:
        print("Error: unable to start thread")






window = tk.Tk()
window.geometry("240x450")
window.title('主控板测试')

###通道1
labelFrame_Ch1 = tk.LabelFrame(window, fg = 'blue', bg = 'white', text = "通道1")
labelFrame_Ch1.grid(row=0, column = 0)

label_Ch1_title_sn = tk.Label(labelFrame_Ch1, bg = "white", text = '请输入条码：')
label_Ch1_title_sn.grid(row = 0, column = 0, sticky = 'wn')

entry_Ch1 = tk.Entry(labelFrame_Ch1)
"""entry_Ch1.bind("<Return>", TestStart)"""
entry_Ch1.grid(row = 0, column = 1)

label_Ch1_title_power = tk.Label(labelFrame_Ch1, bg = "white", text = 'power：')
label_Ch1_title_power.grid(row = 1, column = 0, sticky = 'wn')

label_Ch1_value_power = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_power.grid(row = 1, column = 1, sticky = 'wn')

label_Ch1_title_current = tk.Label(labelFrame_Ch1, bg = "white", text = '12V_Current：')
label_Ch1_title_current.grid(row = 2, column = 0, sticky = 'wn')

label_Ch1_value_current = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_current.grid(row = 2, column = 1, sticky = 'wn')



label_Ch1_title_adctest = tk.Label(labelFrame_Ch1, bg = "white", text = 'adctest：')
label_Ch1_title_adctest.grid(row = 3, column = 0, sticky = 'wn')

label_Ch1_value_adctest = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_adctest.grid(row = 3, column = 1, sticky = 'wn')

label_Ch1_title_flashtest = tk.Label(labelFrame_Ch1, bg = "white", text = 'flashtest：')
label_Ch1_title_flashtest.grid(row = 4, column = 0, sticky = 'wn')

label_Ch1_value_flashtest = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_flashtest.grid(row = 4, column = 1, sticky = 'wn')


label_Ch1_title_vBat = tk.Label(labelFrame_Ch1, bg = 'white', text = 'VCC_BAT')
label_Ch1_title_vBat.grid(row = 5, column = 0, sticky = 'wn')

label_Ch1_value_vBat = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_vBat.grid(row = 5, column = 1, sticky = 'wn')


label_Ch1_title_eepromtest = tk.Label(labelFrame_Ch1, bg = "white", text = 'eepromtest：')
label_Ch1_title_eepromtest.grid(row = 6, column = 0, sticky = 'wn')

label_Ch1_value_eepromtest = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_eepromtest.grid(row = 6, column = 1, sticky = 'wn')

label_Ch1_title_clocktest = tk.Label(labelFrame_Ch1, bg = "white", text = 'clocktest：')
label_Ch1_title_clocktest.grid(row = 7, column = 0, sticky = 'wn')

label_Ch1_value_clocktest = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_clocktest.grid(row = 7, column = 1, sticky = 'wn')

label_Ch1_title_audiotest = tk.Label(labelFrame_Ch1, bg = "white", text = 'audiotest：')
label_Ch1_title_audiotest.grid(row = 8, column = 0, sticky = 'wn')

label_Ch1_value_audiotest = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_audiotest.grid(row = 8, column = 1, sticky = 'wn')

label_Ch1_title_iotest = tk.Label(labelFrame_Ch1, bg = "white", text = 'iotest：')
label_Ch1_title_iotest.grid(row = 9, column = 0, sticky = 'wn')

label_Ch1_value_iotest = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_iotest.grid(row = 9, column = 1, sticky = 'wn')

label_Ch1_title_buzzertest = tk.Label(labelFrame_Ch1, bg = "white", text = 'buzzertest：')
label_Ch1_title_buzzertest.grid(row = 10, column = 0, sticky = 'wn')

label_Ch1_value_buzzertest = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_buzzertest.grid(row = 10, column = 1, sticky = 'wn')

label_Ch1_title_flash_product = tk.Label(labelFrame_Ch1, bg = "white", text = 'flash_product：')
label_Ch1_title_flash_product.grid(row = 11, column = 0, sticky = 'wn')

label_Ch1_value_flash_product = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_flash_product.grid(row = 11, column = 1, sticky = 'wn')

label_Ch1_process = tk.Label(labelFrame_Ch1,bg = "white", text = '等待测试...')
label_Ch1_process.grid(row = 12, column = 0, sticky = 'wn')


button_start = tk.Button(window,width=33,height=3,text='开始测试',padx=1,pady=1,anchor='c',command=TestStart,)
button_start.grid(row = 13, column = 0, sticky = 'wn')

button_confirm = tk .Button(window,width=33,height=3,text='蜂鸣器信息录入',padx=1,pady=1,anchor='c',command=CPU_buzzertest_confirm,)
button_confirm.grid(row = 14, column = 0, sticky = 'wn')
window.mainloop()
