#coding=utf-8
# -*- coding:utf-8 -*-
import time
import datetime
import smbus
import os
import threading
import csv
import tkinter as tk
import IOExtBrd as IO
import PCF8591 as AD
import Current as Cur
import RPi.GPIO as GPIO
import LogUpload as ftp
import MotoDirection as MOTO
from tkinter import messagebox

LogNameCh2=0
LogNameCh3=0

LogNameCh1=0
LogNameCh2=0
LogNameCh3=0


LogSheetCh1=[]
LogSheetCh2=[]
LogSheetCh3=[]


ChargeResultCh1=0
ChargeResultCh2=0
ChargeResultCh3=0


SerialResultCh1=0
SerialResultCh2=0
SerialResultCh3=0


ChgFinishCh1=0
ChgFinishCh2=0
ChgFinishCh3=0


CurrentCh1List=[]
VSENACh1List=[]
VSENBCh1List=[]

CurrentCh2List=[]
VSENACh2List=[]
VSENBCh2List=[]

CurrentCh3List=[]
VSENACh3List=[]
VSENBCh3List=[]

'''测量数保存数组'''
Current_Ch1_Data =[]
VSENA_Ch1_Data = []
VSENB_Ch1_Data = []

Current_Ch2_Data =[]
VSENA_Ch2_Data = []
VSENB_Ch2_Data = []

Current_Ch3_Data =[]
VSENA_Ch3_Data = []
VSENB_Ch3_Data = []

'''功能是否正常'''
Current_Ch1_Function = 0
VSENA_Ch1_Function = 0
VSENB_Ch1_Function = 0
MotoPosDir_Ch1_Function = 0
MotoNegDir_Ch1_Function = 0
MotoPosSpd_Ch1_Function = 0
MotoNegSpd_Ch1_Function = 0

Current_Ch2_Function = 0
VSENA_Ch2_Function = 0
VSENB_Ch2_Function = 0
MotoPosDir_Ch2_Function = 0
MotoNegDir_Ch2_Function = 0
MotoPosSpd_Ch2_Function = 0
MotoNegSpd_Ch2_Function = 0


Current_Ch3_Function = 0
VSENA_Ch3_Function = 0
VSENB_Ch3_Function = 0
MotoPosDir_Ch3_Function = 0
MotoNegDir_Ch3_Function = 0
MotoPosSpd_Ch3_Function = 0
MotoNegSpd_Ch3_Function = 0


AD1Addr = 0x48
AD2Addr = 0x49
AD3Addr = 0x4a
A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43

sn1_Check_result = 0
sn2_Check_result = 0
sn3_Check_result = 0

ch1_signal = 0
ch2_signal = 0
ch3_signal = 0

signal = 1

def moto_start_test():
    ch1_test = threading.Timer(1, Ch1_MotoINit)
    ch2_test = threading.Timer(1, Ch2_MotoINit)
    ch3_test = threading.Timer(1, Ch3_MotoINit)
    try:
        # test.daemon = True
        # test_main.daemon = True
        # test_face.daemon = True
        ch1_test.start()
        ch2_test.start()
        ch3_test.start()
    except Exception:
        print("Error: unable to start thread")


def RelayStart():
    print("step1:开始测试")
    IO.IOExtInit(0x27)
    IO.IOExtChBWrite(0x27,0xFC)

def EndTest():
    print("step15:结束测试")
    global CurrentCh1List
    global VSENACh1List
    global VSENBCh1List
    global CurrentCh2List
    global VSENACh2List
    global VSENBCh2List
    global CurrentCh3List
    global VSENACh3List
    global VSENBCh3List

    global ChargeResultCh1
    global ChargeResultCh2
    global ChargeResultCh3


    global SerialResultCh1
    global SerialResultCh2
    global SerialResultCh3


    global LogSheetCh1
    global LogSheetCh2
    global LogSheetCh3


    global LogNameCh1
    global LogNameCh2
    global LogNameCh3

    global Current_Ch1_Function
    global VSENA_Ch1_Function
    global VSENB_Ch1_Function
    global MotoPosDir_Ch1_Function
    global MotoNegDir_Ch1_Function
    global MotoPosSpd_Ch1_Function
    global MotoNegSpd_Ch1_Function

    global Current_Ch2_Function
    global VSENA_Ch2_Function
    global VSENB_Ch2_Function
    global MotoPosDir_Ch2_Function
    global MotoNegDir_Ch2_Function
    global MotoPosSpd_Ch2_Function
    global MotoNegSpd_Ch2_Function


    global Current_Ch3_Function
    global VSENA_Ch3_Function
    global VSENB_Ch3_Function
    global MotoPosDir_Ch3_Function
    global MotoNegDir_Ch3_Function
    global MotoPosSpd_Ch3_Function
    global MotoNegSpd_Ch3_Function

    CurrentCh1List
    global VSENACh1List
    global VSENBCh1List

    global CurrentCh2List
    global VSENACh2List
    global VSENBCh2List

    global CurrentCh3List
    global VSENACh3List
    global VSENBCh3List

    global Current_Ch1_Data
    global VSENA_Ch1_Data
    global VSENB_Ch1_Data

    global Current_Ch2_Data
    global VSENA_Ch2_Data
    global VSENB_Ch2_Data

    global Current_Ch3_Data
    global VSENA_Ch3_Data
    global VSENB_Ch3_Data

    global ch1_signal
    global ch2_signal
    global ch3_signal

    ch1_signal = 0
    ch2_signal = 0
    ch3_signal = 0

    Current_Ch1_Function = 0
    VSENA_Ch1_Function = 0
    VSENB_Ch1_Function = 0
    MotoPosDir_Ch1_Function = 0
    MotoNegDir_Ch1_Function = 0
    MotoPosSpd_Ch1_Function = 0
    MotoNegSpd_Ch1_Function = 0

    Current_Ch2_Function = 0
    VSENA_Ch2_Function = 0
    VSENB_Ch2_Function = 0
    MotoPosDir_Ch2_Function = 0
    MotoNegDir_Ch2_Function = 0
    MotoPosSpd_Ch2_Function = 0
    MotoNegSpd_Ch2_Function = 0


    Current_Ch3_Function = 0
    VSENA_Ch3_Function = 0
    VSENB_Ch3_Function = 0
    MotoPosDir_Ch3_Function = 0
    MotoNegDir_Ch3_Function = 0
    MotoPosSpd_Ch3_Function = 0
    MotoNegSpd_Ch3_Function = 0

    CurrentCh1List=[]
    VSENACh1List=[]
    VSENBCh1List=[]

    CurrentCh2List=[]
    VSENACh2List=[]
    VSENBCh2List=[]

    CurrentCh3List=[]
    VSENACh3List=[]
    VSENBCh3List=[]

    '''测量数保存数组'''
    Current_Ch1_Data =[]
    VSENA_Ch1_Data = []
    VSENB_Ch1_Data = []

    Current_Ch2_Data =[]
    VSENA_Ch2_Data = []
    VSENB_Ch2_Data = []

    Current_Ch3_Data =[]
    VSENA_Ch3_Data = []
    VSENB_Ch3_Data = []

    IO.IOExtInit(0x27)
    IO.IOExtChBWrite(0x27,0x00)
    label_Ch1_process['text'] = '测试完成'
    label_Ch1_process['bg'] = 'green'

    label_Ch2_process['text'] = '测试完成'
    label_Ch2_process['bg'] = 'green'

    label_Ch3_process['text'] = '测试完成'
    label_Ch3_process['bg'] = 'green'


'''
def GPIOInit():
    print("step2:端口初始化...")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) ##GPIO.BCM
    GPIO.setup(33,GPIO.OUT)  ## Ch1_SM_STEP#
    GPIO.setup(35,GPIO.OUT)  ## Ch2_SM_STEP#
    GPIO.setup(37,GPIO.OUT)  ## Ch3_SM_STEP#

    GPIO.setup(40,GPIO.OUT)  ## Ch1_SM_DIR#
    GPIO.setup(36,GPIO.OUT)  ## Ch1_SM_EN#
    GPIO.setup(16,GPIO.OUT)  ## Ch2_SM_DIR#
    GPIO.setup(12,GPIO.OUT)  ## Ch2_SM_EN#
    GPIO.setup(22,GPIO.OUT)  ## Ch3_SM_DIR#
    GPIO.setup(18,GPIO.OUT)  ## Ch3_SM_EN#

    GPIO.setup(7,GPIO.IN)    ## Ch1_MOTPOS1#
    GPIO.setup(11,GPIO.IN)   ## Ch1_MOTPOS2#
    GPIO.setup(13,GPIO.IN)   ## Ch2_MOTPOS1#
    GPIO.setup(15,GPIO.IN)   ## Ch2_MOTPOS2#
    GPIO.setup(29,GPIO.IN)   ## Ch3_MOTPOS1#
    GPIO.setup(31,GPIO.IN)   ## Ch3_MOTPOS2#
'''
#step3:通道1端口初始化
def Ch1_MotoINit():
    MOTO.MotoPortInit(33,36,40,38,11)
    Ch1_MotoTest()

#step5:通道2端口初始化
def Ch2_MotoINit():
    MOTO.MotoPortInit(35,12,16,13,15)
    Ch2_MotoTest()

#step7:通道3端口初始化
def Ch3_MotoINit():
    MOTO.MotoPortInit(37,18,22,29,31)
    Ch3_MotoTest()

#step4:通道1电机测试
def Ch1_MotoTest():
    global MotoPosDir_Ch1_Function
    global MotoNegDir_Ch1_Function
    global MotoPosSpd_Ch1_Function
    global MotoNegSpd_Ch1_Function
    global ch1_signal
    MOTO.MotoPosInit(33,40,38,11,label_Ch1_value_PosDir)
    time.sleep(0.5)
    MOTO.MotoPosDirTest(33,40,38,11,label_Ch1_value_PosDir)
    time.sleep(0.5)
    MOTO.MotoPosInit_NEGDIR(33,40,38,11,label_Ch1_value_NegDir)
    time.sleep(0.5)
    MOTO.MotoNegDirTest(33,40,38,11,label_Ch1_value_NegDir)
    time.sleep(0.5)
    MOTO.MotoPosInit(33,40,38,11,label_Ch1_value_PosDirSpd)
    time.sleep(0.5)
    MOTO.MotoPosSpdTest(33,40,38,11,label_Ch1_value_PosDirSpd, 1600)
    time.sleep(0.5)
    MOTO.MotoPosInit_NEGDIR(33,40,38,11,label_Ch1_value_NegDirSpd)
    time.sleep(0.5)
    MOTO.MotoNegSpdTest(33,40,38,11,label_Ch1_value_NegDirSpd, 1600)
    ch1_signal = 1

#step6:通道2电机测试
def Ch2_MotoTest():
    global MotoPosDir_Ch2_Function
    global MotoNegDir_Ch2_Function
    global MotoPosSpd_Ch2_Function
    global MotoNegSpd_Ch2_Function
    global ch2_signal
    MOTO.MotoPosInit(35,16,13,15,label_Ch2_value_PosDir)
    time.sleep(0.5)
    MOTO.MotoPosDirTest(35,16,13,15,label_Ch2_value_PosDir)
    time.sleep(0.5)
    MOTO.MotoPosInit_NEGDIR(35,16,13,15,label_Ch2_value_NegDir)
    time.sleep(0.5)
    MOTO.MotoNegDirTest(35,16,13,15,label_Ch2_value_NegDir)
    time.sleep(0.5)
    MOTO.MotoPosInit(35,16,13,15,label_Ch2_value_PosDirSpd)
    time.sleep(0.5)
    MOTO.MotoPosSpdTest(35,16,13,15,label_Ch2_value_PosDirSpd, 1600)
    time.sleep(0.5)
    MOTO.MotoPosInit_NEGDIR(35,16,13,15,label_Ch2_value_NegDirSpd)
    time.sleep(0.5)
    MOTO.MotoNegSpdTest(35,16,13,15,label_Ch2_value_NegDirSpd, 1600)
    ch2_signal = 1

#step8:通道3电机测试
def Ch3_MotoTest():
    global MotoPosDir_Ch3_Function
    global MotoNegDir_Ch3_Function
    global MotoPosSpd_Ch3_Function
    global MotoNegSpd_Ch3_Function
    global ch3_signal
    MOTO.MotoPosInit(37,22,29,31,label_Ch3_value_PosDir)
    time.sleep(0.5)
    MOTO.MotoPosDirTest(37,22,29,31,label_Ch3_value_PosDir)
    time.sleep(0.5)
    MOTO.MotoPosInit_NEGDIR(37,22,29,31,label_Ch3_value_NegDir)
    time.sleep(0.5)
    MOTO.MotoNegDirTest(37,22,29,31,label_Ch3_value_NegDir)
    time.sleep(0.5)
    MOTO.MotoPosInit(37,22,29,31,label_Ch3_value_PosDirSpd)
    time.sleep(0.5)
    MOTO.MotoPosSpdTest(37,22,29,31,label_Ch3_value_PosDirSpd, 1600)
    time.sleep(0.5)
    MOTO.MotoPosInit_NEGDIR(37,22,29,31,label_Ch3_value_NegDirSpd)
    time.sleep(0.5)
    MOTO.MotoNegSpdTest(37,22,29,31,label_Ch3_value_NegDirSpd, 1600)
    ch3_signal = 1

#step2:编号检测
def ChkSN():
    global sn1_Check_result
    global sn2_Check_result
    global sn3_Check_result
    sn_Check_result = 0
    sn1 = entry_Ch1.get()
    sn2 = entry_Ch2.get()
    sn3 = entry_Ch3.get()

    if sn1[0:3] != "JP6":
        entry_Ch1['bg'] = 'red'
        sn1_Check_result=0
    else:
        sn1_Check_result=1
    if sn2[0:3] != "JP6":
        entry_Ch2['bg'] = 'red'
        sn2_Check_result=0
    else:
        sn2_Check_result=1
    if sn3[0:3] != "JP6":
        entry_Ch3['bg'] = 'red'
        sn3_Check_result=0
    else:
        sn3_Check_result=1
    if sn1_Check_result==1 and sn2_Check_result==1 and sn3_Check_result==1 :
        sn_Check_result = 1
    else:
        sn_Check_result = 0
    return sn_Check_result

#step10:电压电流测试
def CurVolTest():
    for i in range(10):
###Ch1_Voltage
        VSENA_Ch1=AD.voltage(AD2Addr,A0)
        print('VSENA_Ch1',VSENA_Ch1)
        VSENB_Ch1=AD.voltage(AD2Addr,A1)
        print('VSENA_Ch1',VSENB_Ch1)
        VSENA_Ch1_Data.append(VSENA_Ch1)
        VSENB_Ch1_Data.append(VSENB_Ch1)
###Ch2_Voltage
        VSENA_Ch2=AD.voltage(AD2Addr,A2)
        print('VSENA_Ch2',VSENA_Ch2)
        VSENB_Ch2=AD.voltage(AD2Addr,A3)
        print('VSENA_Ch2',VSENB_Ch2)
        VSENA_Ch2_Data.append(VSENA_Ch2)
        VSENB_Ch2_Data.append(VSENB_Ch2)
###Ch3_Voltage
        VSENA_Ch3=AD.voltage(AD3Addr,A0)
        print('VSENA_Ch3',VSENA_Ch3)
        VSENB_Ch3=AD.voltage(AD3Addr,A1)
        print('VSENA_Ch3',VSENB_Ch3)
        VSENA_Ch3_Data.append(VSENA_Ch3)
        VSENB_Ch3_Data.append(VSENB_Ch3)
###Ch1_Current
        Voltage_Ch1=AD.voltage(AD1Addr,A0)
        CurValue_Ch1 = 20*Voltage_Ch1
        Current_Ch1_Data.append(CurValue_Ch1)
        print("Voltage_Ch1",Voltage_Ch1)
        print("CurValue_Ch1",CurValue_Ch1)
##Ch2_Current
        Voltage_Ch2=AD.voltage(AD1Addr,A1)
        CurValue_Ch2 = 20*Voltage_Ch2
        Current_Ch2_Data.append(CurValue_Ch2)
        print("Voltage_Ch2",Voltage_Ch2)
        print("CurValue_Ch2",CurValue_Ch2)
##Ch3_Current
        Voltage_Ch3=AD.voltage(AD1Addr,A2)
        CurValue_Ch3 = 20*Voltage_Ch3
        Current_Ch3_Data.append(CurValue_Ch3)
        print("Voltage_Ch3",Voltage_Ch3)
        print("CurValue_Ch3",CurValue_Ch3)
        time.sleep(0.1)

#step11:电压电流数据处理
def SortData():
    global label_Ch1_value_CurValue
    global label_Ch2_value_CurValue
    global label_Ch3_value_CurValue
    global label_Ch1_value_VSENA
    global label_Ch1_value_VSENB
    global label_Ch2_value_VSENA
    global label_Ch2_value_VSENB
    global label_Ch3_value_VSENA
    global label_Ch3_value_VSENB
    global Current_Ch1_Function
    global Current_Ch2_Function
    global Current_Ch3_Function
    global VSENA_Ch1_Function
    global VSENB_Ch1_Function
    global VSENA_Ch2_Function
    global VSENB_Ch2_Function
    global VSENA_Ch3_Function
    global VSENB_Ch3_Function

    VSENA_Ch1_Data.sort()
    VSENB_Ch1_Data.sort()
    VSENA_Ch2_Data.sort()
    VSENB_Ch2_Data.sort()
    VSENA_Ch3_Data.sort()
    VSENB_Ch3_Data.sort()

    Current_Ch1_Data.sort()
    Current_Ch1_MaxData = Current_Ch1_Data[9]
    Current_Ch2_Data.sort()
    Current_Ch2_MaxData = Current_Ch2_Data[9]
    Current_Ch3_Data.sort()
    Current_Ch3_MaxData = Current_Ch3_Data[9]

    VSENA_Ch1_MaxData = VSENA_Ch1_Data[9]
    VSENA_Ch1_MinData = VSENA_Ch1_Data[4]
    VSENB_Ch1_MaxData = VSENB_Ch1_Data[9]
    VSENB_Ch1_MinData = VSENB_Ch1_Data[4]

    VSENA_Ch2_MaxData = VSENA_Ch2_Data[9]
    VSENA_Ch2_MinData = VSENA_Ch2_Data[4]
    VSENB_Ch2_MaxData = VSENB_Ch2_Data[9]
    VSENB_Ch2_MinData = VSENB_Ch2_Data[4]

    VSENA_Ch3_MaxData = VSENA_Ch3_Data[9]
    VSENA_Ch3_MinData = VSENA_Ch3_Data[4]
    VSENB_Ch3_MaxData = VSENB_Ch3_Data[9]
    VSENB_Ch3_MinData = VSENB_Ch3_Data[4]

    print("Current_Ch1_Data[9]=",Current_Ch1_MaxData)
    print("VSENA_Ch1_Data[4]=",VSENA_Ch1_MinData)
    print("VSENA_Ch1_Data[9]=",VSENA_Ch1_MaxData)
    print("VSENB_Ch1_Data[4]=",VSENB_Ch1_MinData)
    print("VSENB_Ch1_Data[9]=",VSENB_Ch1_MaxData)

    print("Current_Ch2_Data[9]=",Current_Ch2_MaxData)
    print("VSENA_Ch2_Data[4]=",VSENA_Ch2_MinData)
    print("VSENA_Ch2_Data[9]=",VSENA_Ch2_MaxData)
    print("VSENB_Ch2_Data[4]=",VSENB_Ch2_MinData)
    print("VSENB_Ch2_Data[9]=",VSENB_Ch2_MaxData)

    print("Current_Ch3_Data[9]=",Current_Ch3_MaxData)
    print("VSENA_Ch3_Data[4]=",VSENA_Ch3_MinData)
    print("VSENA_Ch3_Data[9]=",VSENA_Ch3_MaxData)
    print("VSENB_Ch3_Data[4]=",VSENB_Ch3_MinData)
    print("VSENB_Ch3_Data[9]=",VSENB_Ch3_MaxData)
###Ch1
    if (Current_Ch1_MaxData >= 10 and Current_Ch1_MaxData <= 20 ):
        label_Ch1_value_CurValue['text'] = "PASS"
        label_Ch1_value_CurValue['bg'] = "green"
        Current_Ch1_Function =  "PASS"
    else:
        label_Ch1_value_CurValue['text'] = "FAIL"
        label_Ch1_value_CurValue['bg'] = "red"
        Current_Ch1_Function =  "NG"

    if (VSENA_Ch1_MinData >= 0 and VSENA_Ch1_MaxData <= 4):
        label_Ch1_value_VSENA['text'] = "PASS"
        label_Ch1_value_VSENA['bg'] = "green"
        VSENA_Ch1_Function =  "PASS"
    else:
        label_Ch1_value_VSENA['text'] = "FAIL"
        label_Ch1_value_VSENA['bg'] = "red"
        VSENA_Ch1_Function =  "NG"

    if (VSENB_Ch1_MinData >= 0 and VSENB_Ch1_MaxData <= 4):
        label_Ch1_value_VSENB['text'] = "PASS"
        label_Ch1_value_VSENB['bg'] = "green"
        VSENB_Ch1_Function =  "PASS"
    else:
        label_Ch1_value_VSENB['text'] = "FAIL"
        label_Ch1_value_VSENB['bg'] = "red"
        VSENB_Ch1_Function =  "NG"
###Ch2
    if (Current_Ch2_MaxData >= 10 and Current_Ch2_MaxData <= 20 ):
        label_Ch2_value_CurValue['text'] = "PASS"
        label_Ch2_value_CurValue['bg'] = "green"
        Current_Ch2_Function =  "PASS"
    else:
        label_Ch2_value_CurValue['text'] = "FAIL"
        label_Ch2_value_CurValue['bg'] = "red"
        Current_Ch2_Function =  "NG"

    if (VSENA_Ch2_MinData >= 0 and VSENA_Ch2_MaxData <= 4):
        label_Ch2_value_VSENA['text'] = "PASS"
        label_Ch2_value_VSENA['bg'] = "green"
        VSENA_Ch2_Function =  "PASS"
    else:
        label_Ch2_value_VSENA['text'] = "FAIL"
        label_Ch2_value_VSENA['bg'] = "red"
        VSENA_Ch2_Function =  "NG"

    if (VSENB_Ch2_MinData >= 0 and VSENB_Ch2_MaxData <= 4):
        label_Ch2_value_VSENB['text'] = "PASS"
        label_Ch2_value_VSENB['bg'] = "green"
        VSENB_Ch2_Function =  "PASS"
    else:
        label_Ch2_value_VSENB['text'] = "FAIL"
        label_Ch2_value_VSENB['bg'] = "red"
        VSENB_Ch2_Function =  "NG"
###Ch3
    if (Current_Ch3_MaxData >= 10 and Current_Ch3_MaxData <= 20 ):
        label_Ch3_value_CurValue['text'] = "PASS"
        label_Ch3_value_CurValue['bg'] = "green"
        Current_Ch3_Function =  "PASS"
    else:
        label_Ch3_value_CurValue['text'] = "FAIL"
        label_Ch3_value_CurValue['bg'] = "red"
        Current_Ch3_Function =  "NG"

    if (VSENA_Ch3_MinData >= 0 and VSENA_Ch3_MaxData <= 4):
        label_Ch3_value_VSENA['text'] = "PASS"
        label_Ch3_value_VSENA['bg'] = "green"
        VSENA_Ch3_Function =  "PASS"
    else:
        label_Ch3_value_VSENA['text'] = "FAIL"
        label_Ch3_value_VSENA['bg'] = "red"
        VSENA_Ch3_Function =  "NG"

    if (VSENB_Ch3_MinData >= 0 and VSENB_Ch3_MaxData <= 4):
        label_Ch3_value_VSENB['text'] = "PASS"
        label_Ch3_value_VSENB['bg'] = "green"
        VSENB_Ch3_Function =  "PASS"
    else:
        label_Ch3_value_VSENB['text'] = "FAIL"
        label_Ch3_value_VSENB['bg'] = "red"
        VSENB_Ch3_Function =  "NG"

#step12:电压电流数据处理对应结果
def MotoFunction():
    global MotoPosDir_Ch1_Function
    global MotoNegDir_Ch1_Function
    global MotoPosSpd_Ch1_Function
    global MotoNegSpd_Ch1_Function

    global MotoPosDir_Ch2_Function
    global MotoNegDir_Ch2_Function
    global MotoPosSpd_Ch2_Function
    global MotoNegSpd_Ch2_Function

    global MotoPosDir_Ch3_Function
    global MotoNegDir_Ch3_Function
    global MotoPosSpd_Ch3_Function
    global MotoNegSpd_Ch3_Function

    MotoPosDir_Ch1_Function = label_Ch1_value_PosDir['text']
    MotoNegDir_Ch1_Function = label_Ch1_value_NegDir['text']
    MotoPosSpd_Ch1_Function = label_Ch1_value_PosDirSpd['text']
    MotoNegSpd_Ch1_Function = label_Ch1_value_NegDirSpd['text']

    MotoPosDir_Ch2_Function = label_Ch2_value_PosDir['text']
    MotoNegDir_Ch2_Function = label_Ch2_value_NegDir['text']
    MotoPosSpd_Ch2_Function = label_Ch2_value_PosDirSpd['text']
    MotoNegSpd_Ch2_Function = label_Ch2_value_NegDirSpd['text']

    MotoPosDir_Ch3_Function = label_Ch3_value_PosDir['text']
    MotoNegDir_Ch3_Function = label_Ch3_value_NegDir['text']
    MotoPosSpd_Ch3_Function = label_Ch3_value_PosDirSpd['text']
    MotoNegSpd_Ch3_Function = label_Ch3_value_NegDirSpd['text']

#step13:测试数据保存
def LogProcess():
    print("step7: 记录处理...")
    global CurrentCh1List
    global VSENACh1List
    global VSENBCh1List
    global CurrentCh2List
    global VSENACh2List
    global VSENBCh2List
    global CurrentCh3List
    global VSENACh3List
    global VSENBCh3List

    global ChargeResultCh1
    global ChargeResultCh2
    global ChargeResultCh3


    global SerialResultCh1
    global SerialResultCh2
    global SerialResultCh3


    global LogSheetCh1
    global LogSheetCh2
    global LogSheetCh3


    global LogNameCh1
    global LogNameCh2
    global LogNameCh3

    global Current_Ch1_Function
    global VSENA_Ch1_Function
    global VSENB_Ch1_Function
    global MotoPosDir_Ch1_Function
    global MotoNegDir_Ch1_Function
    global MotoPosSpd_Ch1_Function
    global MotoNegSpd_Ch1_Function
###Ch1
    LogSheetCh1.append(["Current Value(mA):"])
    LogSheetCh1.append(Current_Ch1_Data)
    LogSheetCh1.append(["VSENA_Ch1 Value(V):"])
    LogSheetCh1.append(VSENA_Ch1_Data)
    LogSheetCh1.append(["VSENB_Ch1 Value(V):"])
    LogSheetCh1.append(VSENB_Ch1_Data)
    LogSheetCh1.append(["Current_Ch1 Function"])
    LogSheetCh1.append([Current_Ch1_Function])
    LogSheetCh1.append(["VSENA_Ch1 Function"])
    LogSheetCh1.append([VSENA_Ch1_Function])
    LogSheetCh1.append(["VSENB_Ch1 Function"])
    LogSheetCh1.append([VSENB_Ch1_Function])
    LogSheetCh1.append(["MotoPosDir_Ch1 Function"])
    LogSheetCh1.append([MotoPosDir_Ch1_Function])
    LogSheetCh1.append(["MotoNegDir_Ch1 Function"])
    LogSheetCh1.append([MotoNegDir_Ch1_Function])
    LogSheetCh1.append(["MotoPosSpd_Ch1 Function"])
    LogSheetCh1.append([MotoPosSpd_Ch1_Function])
    LogSheetCh1.append(["MotoNegSpd_Ch1 Function"])
    LogSheetCh1.append([MotoNegSpd_Ch1_Function])
    LogSheetCh1.append(["End time:"])
    EndTime = datetime.datetime.now()
    LogSheetCh1.append([EndTime.strftime("%Y-%m-%d %H:%M:%S")])
###Ch2
    LogSheetCh2.append(["Current Value(mA):"])
    LogSheetCh2.append(Current_Ch2_Data)
    LogSheetCh2.append(["VSENA_Ch2 Value(V):"])
    LogSheetCh2.append(VSENA_Ch2_Data)
    LogSheetCh2.append(["VSENB_Ch2 Value(V):"])
    LogSheetCh2.append(VSENB_Ch2_Data)
    LogSheetCh2.append(["Current_Ch2 Function"])
    LogSheetCh2.append([Current_Ch2_Function])
    LogSheetCh2.append(["VSENA_Ch2 Function"])
    LogSheetCh2.append([VSENA_Ch2_Function])
    LogSheetCh2.append(["VSENB_Ch2 Function"])
    LogSheetCh2.append([VSENB_Ch2_Function])
    LogSheetCh2.append(["MotoPosDir_Ch2 Function"])
    LogSheetCh2.append([MotoPosDir_Ch2_Function])
    LogSheetCh2.append(["MotoNegDir_Ch2 Function"])
    LogSheetCh2.append([MotoNegDir_Ch2_Function])
    LogSheetCh2.append(["MotoPosSpd_Ch2 Function"])
    LogSheetCh2.append([MotoPosSpd_Ch2_Function])
    LogSheetCh2.append(["MotoNegSpd_Ch2 Function"])
    LogSheetCh2.append([MotoNegSpd_Ch2_Function])
    LogSheetCh2.append(["End time:"])
    EndTime = datetime.datetime.now()
    LogSheetCh2.append([EndTime.strftime("%Y-%m-%d %H:%M:%S")])
###Ch3
    LogSheetCh3.append(["Current Value(mA):"])
    LogSheetCh3.append(Current_Ch3_Data)
    LogSheetCh3.append(["VSENA_Ch3 Value(V):"])
    LogSheetCh3.append(VSENA_Ch3_Data)
    LogSheetCh3.append(["VSENB_Ch3 Value(V):"])
    LogSheetCh3.append(VSENB_Ch3_Data)
    LogSheetCh3.append(["Current_Ch3 Function"])
    LogSheetCh3.append([Current_Ch3_Function])
    LogSheetCh3.append(["VSENA_Ch3 Function"])
    LogSheetCh3.append([VSENA_Ch3_Function])
    LogSheetCh3.append(["VSENB_Ch3 Function"])
    LogSheetCh3.append([VSENB_Ch3_Function])
    LogSheetCh3.append(["MotoPosDir_Ch3 Function"])
    LogSheetCh3.append([MotoPosDir_Ch3_Function])
    LogSheetCh3.append(["MotoNegDir_Ch3 Function"])
    LogSheetCh3.append([MotoNegDir_Ch3_Function])
    LogSheetCh3.append(["MotoPosSpd_Ch3 Function"])
    LogSheetCh3.append([MotoPosSpd_Ch3_Function])
    LogSheetCh3.append(["MotoNegSpd_Ch3 Function"])
    LogSheetCh3.append([MotoNegSpd_Ch3_Function])
    LogSheetCh3.append(["End time:"])
    EndTime = datetime.datetime.now()
    LogSheetCh3.append([EndTime.strftime("%Y-%m-%d %H:%M:%S")])

    writeFileObj = open("/home/pi/Desktop/work/Finalversion/Moto/" + LogNameCh1 + ".csv", "w", newline="")
    writer = csv.writer(writeFileObj)
    for row in LogSheetCh1:
        writer.writerow([row])
    writeFileObj.close()
    time.sleep(0.1)
    ftp.LogUpload(LogNameCh1)

    writeFileObj = open("/home/pi/Desktop/work/Finalversion/Moto/" + LogNameCh2 + ".csv", "w", newline="")
    writer = csv.writer(writeFileObj)
    for row in LogSheetCh2:
        writer.writerow([row])
    writeFileObj.close()
    time.sleep(0.1)
    ftp.LogUpload(LogNameCh2)

    writeFileObj = open("/home/pi/Desktop/work/Finalversion/Moto/" + LogNameCh3 + ".csv", "w", newline="")
    writer = csv.writer(writeFileObj)
    for row in LogSheetCh3:
        writer.writerow([row])
    writeFileObj.close()
    time.sleep(0.1)
    ftp.LogUpload(LogNameCh3)


#程序开始
def TestProcess():
    global LogSheetCh1
    global LogSheetCh2
    global LogSheetCh3

    global LogNameCh1
    global LogNameCh2
    global LogNameCh3
    global ch1_signal
    global ch2_signal
    global ch3_signal

    global signal

    LogSheetCh1=[]
    LogSheetCh2=[]
    LogSheetCh3=[]

    LogNameCh1=0
    LogNameCh2=0
    LogNameCh3=0

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

    LogNameCh3 = entry_Ch3.get()
    LogSheetCh3.append(["PartNO:"])
    LogSheetCh3.append([LogNameCh1])

    LogSheetCh3.append(["Start time:"])
    StartTime = datetime.datetime.now()
    LogSheetCh3.append([StartTime.strftime("%Y-%m-%d %H:%M:%S")])

    label_Ch1_process['text'] = '测试中...'
    label_Ch1_process['bg'] = 'yellow'

    label_Ch2_process['text'] = '测试中...'
    label_Ch2_process['bg'] = 'yellow'

    label_Ch3_process['text'] = '测试中...'
    label_Ch3_process['bg'] = 'yellow'
    RelayStart()      #step1
    signal = 1
    # GPIOInit()
    '''
    Ch1_MotoINit()
    Ch2_MotoINit()     #step5
    Ch3_MotoINit()     #step7

    while True:
        print("GPIO 13",GPIO.input(29))
        print("GPIO 15",GPIO.input(31))
        time.sleep(1)
    '''
    if ChkSN() == 1:       #step2
    '''
        Ch1_MotoINit()     #step3
        Ch1_MotoTest()     #step4

        Ch2_MotoINit()     #step5
        Ch2_MotoTest()     #step6

        Ch3_MotoINit()     #step7
        Ch3_MotoTest()     #step8
    '''
        moto_start_test()
        while signal = 1:
            if ch1_signal == 1 and ch2_signal == 1 and ch3_signal == 1:

                p = GPIO.PWM(33, 1000)  #(ChANEL, FREQ) #step9
                p.start(15)   #(DUTY)
                q = GPIO.PWM(35, 1000)  #(ChANEL, FREQ)
                q.start(15)   #(DUTY)
                z = GPIO.PWM(37, 1000)  #(ChANEL, FREQ)
                z.start(15)   #(DUTY)
                CurVolTest()                        #step10
                SortData()                          #step11
                MotoFunction()                      #step12
                LogProcess()                       #step13
                #MOTO.MotoRun(33,40,0)
                signal = 0
                EndTest()                      #step14
            else:
                signal = 1
    else:

        label_Ch1_process['text'] = '请输入条码'
        label_Ch1_process['bg'] = 'red'

        label_Ch2_process['text'] = '请输入条码'
        label_Ch2_process['bg'] = 'red'

        label_Ch3_process['text'] = '请输入条码'
        label_Ch3_process['bg'] = 'red'

        IO.IOExtInit(0x27)
        IO.IOExtChBWrite(0x27,0x00)
        messagebox.showinfo("错误", "请输入合法的条码")

def TestStart():

    label_Ch1_value_CurValue['text'] = '???'
    label_Ch1_value_VSENA['text'] = '???'
    label_Ch1_value_VSENB['text'] = '???'
    label_Ch1_value_PosDir['text'] = '???'
    label_Ch1_value_NegDir['text'] = '???'
    label_Ch1_value_PosDirSpd['text'] = '???'
    label_Ch1_value_NegDirSpd['text'] = '???'

    label_Ch1_value_CurValue['bg'] = 'white'
    label_Ch1_value_VSENA['bg'] = 'white'
    label_Ch1_value_VSENB['bg'] = 'white'
    label_Ch1_value_PosDir['bg'] = 'white'
    label_Ch1_value_NegDir['bg'] = 'white'
    label_Ch1_value_PosDirSpd['bg'] = 'white'
    label_Ch1_value_NegDirSpd['bg'] = 'white'

    label_Ch2_value_CurValue['text'] = '???'
    label_Ch2_value_VSENA['text'] = '???'
    label_Ch2_value_VSENB['text'] = '???'
    label_Ch2_value_PosDir['text'] = '???'
    label_Ch2_value_NegDir['text'] = '???'
    label_Ch2_value_PosDirSpd['text'] = '???'
    label_Ch2_value_NegDirSpd['text'] = '???'

    label_Ch2_value_CurValue['bg'] = 'white'
    label_Ch2_value_VSENA['bg'] = 'white'
    label_Ch2_value_VSENB['bg'] = 'white'
    label_Ch2_value_PosDir['bg'] = 'white'
    label_Ch2_value_NegDir['bg'] = 'white'
    label_Ch2_value_PosDirSpd['bg'] = 'white'
    label_Ch2_value_NegDirSpd['bg'] = 'white'

    label_Ch3_value_CurValue['text'] = '???'
    label_Ch3_value_VSENA['text'] = '???'
    label_Ch3_value_VSENB['text'] = '???'
    label_Ch3_value_PosDir['text'] = '???'
    label_Ch3_value_NegDir['text'] = '???'
    label_Ch3_value_PosDirSpd['text'] = '???'
    label_Ch3_value_NegDirSpd['text'] = '???'

    label_Ch3_value_CurValue['bg'] = 'white'
    label_Ch3_value_VSENA['bg'] = 'white'
    label_Ch3_value_VSENB['bg'] = 'white'
    label_Ch3_value_PosDir['bg'] = 'white'
    label_Ch3_value_NegDir['bg'] = 'white'
    label_Ch3_value_PosDirSpd['bg'] = 'white'
    label_Ch3_value_NegDirSpd['bg'] = 'white'

    testprocess = threading.Thread(target = TestProcess)

    try:
        testprocess.start()

    except:
        print("Error: unable to start thread")

window = tk.Tk()
window.geometry("855x240")
window.title('电机测试')

###通道1
labelFrame_Ch1 = tk.LabelFrame(window, fg = 'blue', bg = 'white', text = "通道1")
labelFrame_Ch1.grid(row=0, column = 0)

label_Ch1_title_sn = tk.Label(labelFrame_Ch1, bg = "white", text = '请输入条码：')
label_Ch1_title_sn.grid(row = 0, column = 0, sticky = 'wn')

entry_Ch1 = tk.Entry(labelFrame_Ch1)
"""entry_Ch1.bind("<Return>", TestStart)"""
entry_Ch1.grid(row = 0, column = 1)

label_Ch1_title_CurValue = tk.Label(labelFrame_Ch1, bg = "white", text = '总电流值(mA)：')
label_Ch1_title_CurValue.grid(row = 2, column = 0, sticky = 'wn')

label_Ch1_value_CurValue = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_CurValue.grid(row = 2, column = 1, sticky = 'wn')

label_Ch1_title_VSENA = tk.Label(labelFrame_Ch1, bg = "white", text = 'VSENA(V)：')
label_Ch1_title_VSENA.grid(row = 4, column = 0, sticky = 'wn')

label_Ch1_value_VSENA = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_VSENA.grid(row = 4, column = 1, sticky = 'wn')

label_Ch1_title_VSENB = tk.Label(labelFrame_Ch1, bg = "white", text = 'VSENB(V)：')
label_Ch1_title_VSENB.grid(row = 5, column = 0, sticky = 'wn')

label_Ch1_value_VSENB = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_VSENB.grid(row = 5, column = 1, sticky = 'wn')

label_Ch1_title_PosDir = tk.Label(labelFrame_Ch1, bg = "white", text = '电机正转检测：')
label_Ch1_title_PosDir.grid(row = 6, column = 0, sticky = 'wn')

label_Ch1_value_PosDir = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_PosDir.grid(row = 6, column = 1, sticky = 'wn')

label_Ch1_title_NegDir = tk.Label(labelFrame_Ch1, bg = "white", text = '电机反转检测：')
label_Ch1_title_NegDir.grid(row = 7, column = 0, sticky = 'wn')

label_Ch1_value_NegDir = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_NegDir.grid(row = 7, column = 1, sticky = 'wn')

label_Ch1_title_PosDirSpd = tk.Label(labelFrame_Ch1, bg = "white", text = '电机正转速度检测：')
label_Ch1_title_PosDirSpd.grid(row = 8, column = 0, sticky = 'wn')

label_Ch1_value_PosDirSpd = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_PosDirSpd.grid(row = 8, column = 1, sticky = 'wn')

label_Ch1_title_NegDirSpd = tk.Label(labelFrame_Ch1, bg = "white", text = '电机反转速度检测：')
label_Ch1_title_NegDirSpd.grid(row = 9, column = 0, sticky = 'wn')

label_Ch1_value_NegDirSpd = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
label_Ch1_value_NegDirSpd.grid(row = 9, column = 1, sticky = 'wn')

label_Ch1_process = tk.Label(labelFrame_Ch1,bg = "white", text = '等待测试...')
label_Ch1_process.grid(row = 10, column = 0, sticky = 'wn')

###通道2
labelFrame_Ch2 = tk.LabelFrame(window, fg = 'blue', bg = 'white', text = "通道2")
labelFrame_Ch2.grid(row=0, column = 1)

label_Ch2_title_sn = tk.Label(labelFrame_Ch2, bg = "white", text = '请输入条码：')
label_Ch2_title_sn.grid(row = 0, column = 0, sticky = 'wn')

entry_Ch2 = tk.Entry(labelFrame_Ch2)
"""entry_Ch2.bind("<Return>", TestStart)"""
entry_Ch2.grid(row = 0, column = 2)

label_Ch2_title_CurValue = tk.Label(labelFrame_Ch2, bg = "white", text = '总电流值(mA)：')
label_Ch2_title_CurValue.grid(row = 2, column = 0, sticky = 'wn')

label_Ch2_value_CurValue = tk.Label(labelFrame_Ch2, bg = "white", text = '？？？')
label_Ch2_value_CurValue.grid(row = 2, column = 1, sticky = 'wn')

label_Ch2_title_VSENA = tk.Label(labelFrame_Ch2, bg = "white", text = 'VSENA(V)：')
label_Ch2_title_VSENA.grid(row = 4, column = 0, sticky = 'wn')

label_Ch2_value_VSENA = tk.Label(labelFrame_Ch2, bg = "white", text = '？？？')
label_Ch2_value_VSENA.grid(row = 4, column = 1, sticky = 'wn')

label_Ch2_title_VSENB = tk.Label(labelFrame_Ch2, bg = "white", text = 'VSENB(V)：')
label_Ch2_title_VSENB.grid(row = 5, column = 0, sticky = 'wn')

label_Ch2_value_VSENB = tk.Label(labelFrame_Ch2, bg = "white", text = '？？？')
label_Ch2_value_VSENB.grid(row = 5, column = 1, sticky = 'wn')

label_Ch2_title_PosDir = tk.Label(labelFrame_Ch2, bg = "white", text = '电机正转检测：')
label_Ch2_title_PosDir.grid(row = 6, column = 0, sticky = 'wn')

label_Ch2_value_PosDir = tk.Label(labelFrame_Ch2, bg = "white", text = '？？？')
label_Ch2_value_PosDir.grid(row = 6, column = 1, sticky = 'wn')

label_Ch2_title_NegDir = tk.Label(labelFrame_Ch2, bg = "white", text = '电机反转检测：')
label_Ch2_title_NegDir.grid(row = 7, column = 0, sticky = 'wn')

label_Ch2_value_NegDir = tk.Label(labelFrame_Ch2, bg = "white", text = '？？？')
label_Ch2_value_NegDir.grid(row = 7, column = 1, sticky = 'wn')

label_Ch2_title_PosDirSpd = tk.Label(labelFrame_Ch2, bg = "white", text = '电机正转速度检测：')
label_Ch2_title_PosDirSpd.grid(row = 8, column = 0, sticky = 'wn')

label_Ch2_value_PosDirSpd = tk.Label(labelFrame_Ch2, bg = "white", text = '？？？')
label_Ch2_value_PosDirSpd.grid(row = 8, column = 1, sticky = 'wn')

label_Ch2_title_NegDirSpd = tk.Label(labelFrame_Ch2, bg = "white", text = '电机反转速度检测：')
label_Ch2_title_NegDirSpd.grid(row = 9, column = 0, sticky = 'wn')

label_Ch2_value_NegDirSpd = tk.Label(labelFrame_Ch2, bg = "white", text = '？？？')
label_Ch2_value_NegDirSpd.grid(row = 9, column = 1, sticky = 'wn')

label_Ch2_process = tk.Label(labelFrame_Ch2,bg = "white", text = '等待测试...')
label_Ch2_process.grid(row = 10, column = 0, sticky = 'wn')

###通道3
labelFrame_Ch3 = tk.LabelFrame(window, fg = 'blue', bg = 'white', text = "通道3")
labelFrame_Ch3.grid(row=0, column = 2)

label_Ch3_title_code = tk.Label(labelFrame_Ch3, bg = "white", text = '请输入条码：')
label_Ch3_title_code.grid(row = 0, column = 0, sticky = 'wn')

entry_Ch3 = tk.Entry(labelFrame_Ch3)
"""entry_Ch3.bind("<Return>", TestStart)"""
entry_Ch3.grid(row = 0, column = 1)

label_Ch3_title_CurValue = tk.Label(labelFrame_Ch3, bg = "white", text = '总电流值(mA)：')
label_Ch3_title_CurValue.grid(row = 2, column = 0, sticky = 'wn')

label_Ch3_value_CurValue = tk.Label(labelFrame_Ch3, bg = "white", text = '？？？')
label_Ch3_value_CurValue.grid(row = 2, column = 1, sticky = 'wn')

label_Ch3_title_VSENA = tk.Label(labelFrame_Ch3, bg = "white", text = 'VSENA(V)：')
label_Ch3_title_VSENA.grid(row = 4, column = 0, sticky = 'wn')

label_Ch3_value_VSENA = tk.Label(labelFrame_Ch3, bg = "white", text = '？？？')
label_Ch3_value_VSENA.grid(row = 4, column = 1, sticky = 'wn')

label_Ch3_title_VSENB = tk.Label(labelFrame_Ch3, bg = "white", text = 'VSENB(V)：')
label_Ch3_title_VSENB.grid(row = 5, column = 0, sticky = 'wn')

label_Ch3_value_VSENB = tk.Label(labelFrame_Ch3, bg = "white", text = '？？？')
label_Ch3_value_VSENB.grid(row = 5, column = 1, sticky = 'wn')

label_Ch3_title_PosDir = tk.Label(labelFrame_Ch3, bg = "white", text = '电机正转检测：')
label_Ch3_title_PosDir.grid(row = 6, column = 0, sticky = 'wn')

label_Ch3_value_PosDir = tk.Label(labelFrame_Ch3, bg = "white", text = '？？？')
label_Ch3_value_PosDir.grid(row = 6, column = 1, sticky = 'wn')

label_Ch3_title_NegDir = tk.Label(labelFrame_Ch3, bg = "white", text = '电机反转检测：')
label_Ch3_title_NegDir.grid(row = 7, column = 0, sticky = 'wn')

label_Ch3_value_NegDir = tk.Label(labelFrame_Ch3, bg = "white", text = '？？？')
label_Ch3_value_NegDir.grid(row = 7, column = 1, sticky = 'wn')

label_Ch3_title_PosDirSpd = tk.Label(labelFrame_Ch3, bg = "white", text = '电机正转速度检测：')
label_Ch3_title_PosDirSpd.grid(row = 8, column = 0, sticky = 'wn')

label_Ch3_value_PosDirSpd = tk.Label(labelFrame_Ch3, bg = "white", text = '？？？')
label_Ch3_value_PosDirSpd.grid(row = 8, column = 1, sticky = 'wn')

label_Ch3_title_NegDirSpd = tk.Label(labelFrame_Ch3, bg = "white", text = '电机反转速度检测：')
label_Ch3_title_NegDirSpd.grid(row = 9, column = 0, sticky = 'wn')

label_Ch3_value_NegDirSpd = tk.Label(labelFrame_Ch3, bg = "white", text = '？？？')
label_Ch3_value_NegDirSpd.grid(row = 9, column = 1, sticky = 'wn')

label_Ch3_process = tk.Label(labelFrame_Ch3,bg = "white", text = '等待测试...')
label_Ch3_process.grid(row = 10, column = 0, sticky = 'wn')

button_Test = tk.Button(window, width=44, height=3, text='开始测试',padx=1,pady=1,anchor='c',command=TestStart,)
button_Test.grid(row = 1 ,column = 1, sticky = 'wn')

window.mainloop()
