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
import RPi.GPIO as GPIO
import LogUpload as ftp
import USBCamTest1 as Camera
from tkinter import messagebox

LogNameCh1=0
LogNameCh2=0
LogNameCh3=0
LogNameCh4=0
LogNameCh5=0

ImageName=""

LogSheetCh1=[]
LogSheetCh2=[]
LogSheetCh3=[]
LogSheetCh4=[]
LogSheetCh5=[]

Current_Ch1_Function = 0
Current_Ch2_Function = 0
Current_Ch3_Function = 0
Current_Ch4_Function = 0
Current_Ch5_Function = 0

AD1Addr = 0x48
AD2Addr = 0x49
A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43

Current_Ch1_Data =[]
Current_Ch2_Data =[]
Current_Ch3_Data =[]
Current_Ch4_Data =[]
Current_Ch5_Data =[]
    
def ChkSN():
    print("step1: Check SN...")
    sn1_check_result = 0
    sn2_check_result = 0
    sn3_check_result = 0
    sn4_check_result = 0
    sn5_check_result = 0
    sn_check_result = 0
    sn1 = entry_Ch1.get()
    sn2 = entry_Ch2.get()
    sn3 = entry_Ch3.get()
    sn4 = entry_Ch4.get()
    sn5 = entry_Ch5.get()
    
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
    if sn3[0:3] != "JP6":
        entry_Ch3['bg'] = 'red'
        sn3_check_result=0
    else:
        sn3_check_result=1
    if sn4[0:3] != "JP6":
        entry_Ch4['bg'] = 'red'
        sn4_check_result=0
    else:
        sn4_check_result=1
    if sn5[0:3] != "JP6":
        entry_Ch5['bg'] = 'red'
        sn5_check_result=0
    else:
        sn5_check_result=1
    if sn1_check_result==1 and sn2_check_result==1 and sn3_check_result==1 and sn4_check_result==1 and sn5_check_result==1:
        sn_check_result = 1
    else:
        sn_check_result = 0
    return sn_check_result

def PortEnable():
    print("step2:打开继电器")   
    IO.IOExtInit(0x23)
    IO.IOExtChBWrite(0x23,0x3F)

def EndTest():
    print("step8:结束测试")
    global Current_Ch1_Function
    global Current_Ch2_Function
    global Current_Ch3_Function
    global Current_Ch4_Function
    global Current_Ch5_Function
    
    global Current_Ch1_Data
    global Current_Ch2_Data
    global Current_Ch3_Data
    global Current_Ch4_Data
    global Current_Ch5_Data
    
    global LogSheetCh1
    global LogSheetCh2
    global LogSheetCh3
    global LogSheetCh4
    global LogSheetCh5

    global LogNameCh1
    global LogNameCh2
    global LogNameCh3
    global LogNameCh4
    global LogNameCh5
    
    global ImageName
    
    Current_Ch1_Data =[]
    Current_Ch2_Data =[]
    Current_Ch3_Data =[]
    Current_Ch4_Data =[]
    Current_Ch5_Data =[]
    
    LogSheetCh1=[]
    LogSheetCh2=[]
    LogSheetCh3=[]
    LogSheetCh4=[]
    LogSheetCh5=[]

    LogNameCh1=0
    LogNameCh2=0
    LogNameCh3=0
    LogNameCh4=0
    LogNameCh5=0
    
    ImageName=0
    
    IO.IOExtInit(0x23)
    IO.IOExtChBWrite(0x23,0x00)
    label_Ch1_process['text'] = '测试完成'
    label_Ch1_process['bg'] = 'green'

    label_Ch2_process['text'] = '测试完成'
    label_Ch2_process['bg'] = 'green'

    label_Ch3_process['text'] = '测试完成'
    label_Ch3_process['bg'] = 'green'
    
    label_Ch4_process['text'] = '测试完成'
    label_Ch4_process['bg'] = 'green'

    label_Ch5_process['text'] = '测试完成'
    label_Ch5_process['bg'] = 'green'
    
def ALERT():
    label_Ch1_process['text'] = '测试中断'
    label_Ch1_process['bg'] = 'red'

    label_Ch2_process['text'] = '测试中断'
    label_Ch2_process['bg'] = 'red'

    label_Ch3_process['text'] = '测试中断'
    label_Ch3_process['bg'] = 'red'

    label_Ch4_process['text'] = '测试中断'
    label_Ch4_process['bg'] = 'red'

    label_Ch5_process['text'] = '测试中断'
    label_Ch5_process['bg'] = 'red'

def GPIOHIGH():
    print("step3:点亮LED")
#    IO.IOExtInit(0x23)
    IO.IOExtInit(0x27)
    IO.IOExtChAWrite(0x27,0xFF)
    IO.IOExtChBWrite(0x27,0xFF)
    IO.IOExtChAWrite(0x23,0x0F)
    
def CurVolTest():
    print("step5:电流值检测")
    for i in range(10):
###Ch1_Current
        Voltage_Ch1=AD.voltage(AD1Addr,A0)
        CurValue_Ch1 = round(20*Voltage_Ch1,3)
        Current_Ch1_Data.append(CurValue_Ch1)
        print("Voltage_Ch1",Voltage_Ch1)
        print("CurValue_Ch1",CurValue_Ch1)
##Ch2_Current
        Voltage_Ch2=AD.voltage(AD1Addr,A1)
        CurValue_Ch2 = round(20*Voltage_Ch2,3)
        Current_Ch2_Data.append(CurValue_Ch2)
        print("Voltage_Ch2",Voltage_Ch2)
        print("CurValue_Ch2",CurValue_Ch2)
##Ch3_Current
        Voltage_Ch3=AD.voltage(AD1Addr,A2)
        CurValue_Ch3 = round(20*Voltage_Ch3,3)
        Current_Ch3_Data.append(CurValue_Ch3)
        print("Voltage_Ch3",Voltage_Ch3)
        print("CurValue_Ch3",CurValue_Ch3)
        time.sleep(0.1)
###Ch4_Current
        Voltage_Ch4=AD.voltage(AD1Addr,A3)
        CurValue_Ch4 = round(20*Voltage_Ch4,3)
        Current_Ch4_Data.append(CurValue_Ch4)
        print("Voltage_Ch4",Voltage_Ch4)
        print("CurValue_Ch4",CurValue_Ch4)
##Ch2_Current
        Voltage_Ch5=AD.voltage(AD2Addr,A0)
        CurValue_Ch5 = round(20*Voltage_Ch5,3)
        Current_Ch5_Data.append(CurValue_Ch5)
        print("Voltage_Ch5",Voltage_Ch5)
        print("CurValue_Ch5",CurValue_Ch5)
 
def SortData():
    print("step6:电流数据处理")
    global label_Ch1_value_CurValue
    global label_Ch2_value_CurValue
    global label_Ch3_value_CurValue
    global label_Ch4_value_CurValue
    global label_Ch5_value_CurValue
   
    global Current_Ch1_Function
    global Current_Ch2_Function
    global Current_Ch3_Function
    global Current_Ch4_Function
    global Current_Ch5_Function

    Current_Ch1_Data.sort()
    Current_Ch1_MaxData = Current_Ch1_Data[9]
    Current_Ch2_Data.sort()
    Current_Ch2_MaxData = Current_Ch2_Data[9]
    Current_Ch3_Data.sort()
    Current_Ch3_MaxData = Current_Ch3_Data[9]
    Current_Ch4_Data.sort()
    Current_Ch4_MaxData = Current_Ch4_Data[9]
    Current_Ch5_Data.sort()
    Current_Ch5_MaxData = Current_Ch5_Data[9]
    
    print("Current_Ch1_Data[9]=",Current_Ch1_MaxData)  
    print("Current_Ch2_Data[9]=",Current_Ch2_MaxData)
    print("Current_Ch3_Data[9]=",Current_Ch3_MaxData)
    print("Current_Ch4_Data[9]=",Current_Ch4_MaxData)
    print("Current_Ch5_Data[9]=",Current_Ch5_MaxData)
    
###Ch1   
    if (Current_Ch1_MaxData > 19 and Current_Ch1_MaxData <= 21 ):
        label_Ch1_value_CurValue['text'] = "PASS"
        label_Ch1_value_CurValue['bg'] = "green"
        Current_Ch1_Function =  "PASS"
    else:
        label_Ch1_value_CurValue['text'] = "FAIL"
        label_Ch1_value_CurValue['bg'] = "red"
        Current_Ch1_Function =  "NG"
    
###Ch2         
    if (Current_Ch2_MaxData > 19 and Current_Ch2_MaxData <= 21 ):
        label_Ch2_value_CurValue['text'] = "PASS"
        label_Ch2_value_CurValue['bg'] = "green"
        Current_Ch2_Function =  "PASS"
    else:
        label_Ch2_value_CurValue['text'] = "FAIL"
        label_Ch2_value_CurValue['bg'] = "red"
        Current_Ch2_Function =  "NG"

###Ch3         
    if (Current_Ch3_MaxData > 19 and Current_Ch3_MaxData <= 21 ):
        label_Ch3_value_CurValue['text'] = "PASS"
        label_Ch3_value_CurValue['bg'] = "green"
        Current_Ch3_Function =  "PASS"
    else:
        label_Ch3_value_CurValue['text'] = "FAIL"
        label_Ch3_value_CurValue['bg'] = "red"
        Current_Ch3_Function =  "NG"

###Ch4         
    if (Current_Ch4_MaxData > 19 and Current_Ch4_MaxData <= 21 ):
        label_Ch4_value_CurValue['text'] = "PASS"
        label_Ch4_value_CurValue['bg'] = "green"
        Current_Ch4_Function =  "PASS"
    else:
        label_Ch4_value_CurValue['text'] = "FAIL"
        label_Ch4_value_CurValue['bg'] = "red"
        Current_Ch4_Function =  "NG"

###Ch5        
    if (Current_Ch5_MaxData > 19 and Current_Ch5_MaxData <= 21 ):
        label_Ch5_value_CurValue['text'] = "PASS"
        label_Ch5_value_CurValue['bg'] = "green"
        Current_Ch5_Function =  "PASS"
    else:
        label_Ch5_value_CurValue['text'] = "FAIL"
        label_Ch5_value_CurValue['bg'] = "red"
        Current_Ch5_Function =  "NG"
                   
def LogProcess():
    print("step7: 记录处理...")
    global Current_Ch1_Function
    global Current_Ch2_Function
    global Current_Ch3_Function
    global Current_Ch4_Function
    global Current_Ch5_Function
 
    ###Ch1    
    LogSheetCh1.append(["Current Value(mA):"]) 
    LogSheetCh1.append(Current_Ch1_Data)
    LogSheetCh1.append(["Current_Ch1 Function"])
    LogSheetCh1.append([Current_Ch1_Function])
    #LogSheetCh1.append(["Current_Ch1 Function"])
    #LogSheetCh1.append([Current_Ch1_Function])
   
    LogSheetCh1.append(["End time:"])
    EndTime = datetime.datetime.now()
    LogSheetCh1.append([EndTime.strftime("%Y-%m-%d %H:%M:%S")])
    
    ###Ch2    
    LogSheetCh2.append(["Current Value(mA):"]) 
    LogSheetCh2.append(Current_Ch2_Data)
    LogSheetCh2.append(["Current_Ch2 Function"])
    LogSheetCh2.append([Current_Ch2_Function])
#    LogSheetCh2.append(["Current_Ch2 Function"])
#    LogSheetCh2.append([Current_Ch2_Function])
   
    LogSheetCh2.append(["End time:"])
    EndTime = datetime.datetime.now()
    LogSheetCh2.append([EndTime.strftime("%Y-%m-%d %H:%M:%S")])
    
    ###Ch3    
    LogSheetCh3.append(["Current Value(mA):"]) 
    LogSheetCh3.append(Current_Ch3_Data)
    LogSheetCh3.append(["Current_Ch3 Function"])
    LogSheetCh3.append([Current_Ch3_Function])
#    LogSheetCh3.append(["Current_Ch3 Function"])
#    LogSheetCh3.append([Current_Ch3_Function])
   
    LogSheetCh3.append(["End time:"])
    EndTime = datetime.datetime.now()
    LogSheetCh3.append([EndTime.strftime("%Y-%m-%d %H:%M:%S")])
    
    ###Ch4    
    LogSheetCh4.append(["Current Value(mA):"]) 
    LogSheetCh4.append(Current_Ch4_Data)
    LogSheetCh4.append(["Current_Ch4 Function"])
    LogSheetCh4.append([Current_Ch4_Function])
#    LogSheetCh4.append(["Current_Ch4 Function"])
#    LogSheetCh4.append([Current_Ch4_Function])
   
    LogSheetCh4.append(["End time:"])
    EndTime = datetime.datetime.now()
    LogSheetCh4.append([EndTime.strftime("%Y-%m-%d %H:%M:%S")])
    
    ###Ch5    
    LogSheetCh5.append(["Current Value(mA):"]) 
    LogSheetCh5.append(Current_Ch5_Data)
    LogSheetCh5.append(["Current_Ch5 Function"])
    LogSheetCh5.append([Current_Ch5_Function])
#    LogSheetCh5.append(["Current_Ch5 Function"])
#    LogSheetCh5.append([Current_Ch5_Function])
   
    LogSheetCh5.append(["End time:"])
    EndTime = datetime.datetime.now()
    LogSheetCh5.append([EndTime.strftime("%Y-%m-%d %H:%M:%S")])

    writeFileObj = open("/home/pi/Desktop/test/"+LogNameCh1+'.csv','w')
    writer = csv.writer(writeFileObj)
    for row in LogSheetCh1:
        writer.writerow(row)
    writeFileObj.close()
    time.sleep(0.1)
    ftp.LogUpload(LogNameCh1)

    writeFileObj = open("/home/pi/Desktop/test/"+LogNameCh2+'.csv','w')
    writer = csv.writer(writeFileObj)
    for row in LogSheetCh2:
        writer.writerow(row)
    writeFileObj.close()
    time.sleep(0.1)
    ftp.LogUpload(LogNameCh2)

    writeFileObj = open("/home/pi/Desktop/test/"+LogNameCh3+'.csv','w')
    writer = csv.writer(writeFileObj)
    for row in LogSheetCh3:
        writer.writerow(row)
    writeFileObj.close()
    time.sleep(0.1)
    ftp.LogUpload(LogNameCh3)

    writeFileObj = open("/home/pi/Desktop/test/"+LogNameCh4+'.csv','w')
    writer = csv.writer(writeFileObj)
    for row in LogSheetCh4:
        writer.writerow(row)
    writeFileObj.close()
    time.sleep(0.1)
    ftp.LogUpload(LogNameCh4)

    writeFileObj = open("/home/pi/Desktop/test/"+LogNameCh5+'.csv','w')
    writer = csv.writer(writeFileObj)
    for row in LogSheetCh5:
        writer.writerow(row)
    writeFileObj.close()
    time.sleep(0.1)
    ftp.LogUpload(LogNameCh5)
    
    ftp.LogUploadImage(ImageName)

#    os.remove("/home/pi/Desktop/test/"+LogNameCh1+'.csv')
#    os.remove("/home/pi/Desktop/test/"+LogNameCh2+'.csv')
#    os.remove("/home/pi/Desktop/test/"+LogNameCh3+'.csv')
#    os.remove("/home/pi/Desktop/test/"+LogNameCh4+'.csv')
#    os.remove("/home/pi/Desktop/test/"+LogNameCh5+'.csv')
    
def TestProcess():
    global LogSheetCh1
    global LogSheetCh2
    global LogSheetCh3
    global LogSheetCh4
    global LogSheetCh5

    global LogNameCh1
    global LogNameCh2
    global LogNameCh3
    global LogNameCh4
    global LogNameCh5
    
    global ImageName
    
    LogSheetCh1=[]
    LogSheetCh2=[]
    LogSheetCh3=[]
    LogSheetCh4=[]
    LogSheetCh5=[]

    LogNameCh1=0
    LogNameCh2=0
    LogNameCh3=0
    LogNameCh4=0
    LogNameCh5=0
    
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

    LogNameCh4 = entry_Ch4.get()
    LogSheetCh4.append(["PartNO:"])
    LogSheetCh4.append([LogNameCh4])
    
    LogSheetCh4.append(["Start time:"])
    StartTime = datetime.datetime.now()
    LogSheetCh4.append([StartTime.strftime("%Y-%m-%d %H:%M:%S")])

    LogNameCh5 = entry_Ch5.get()
    LogSheetCh5.append(["PartNO:"])
    LogSheetCh5.append([LogNameCh4])
    
    LogSheetCh5.append(["Start time:"])
    StartTime = datetime.datetime.now()
    LogSheetCh5.append([StartTime.strftime("%Y-%m-%d %H:%M:%S")])
    
    ImageName = LogNameCh1 + LogNameCh2 + LogNameCh3 + LogNameCh4 + LogNameCh5

    label_Ch1_process['text'] = '测试中...'
    label_Ch1_process['bg'] = 'yellow'

    label_Ch2_process['text'] = '测试中...'
    label_Ch2_process['bg'] = 'yellow'

    label_Ch3_process['text'] = '测试中...'
    label_Ch3_process['bg'] = 'yellow'

    label_Ch4_process['text'] = '测试中...'
    label_Ch4_process['bg'] = 'yellow'

    label_Ch5_process['text'] = '测试中...'
    label_Ch5_process['bg'] = 'yellow'
         
    if ChkSN() == 1:             #step1
        PortEnable()             #step2        
        GPIOHIGH()               #step3
        Camera.Camera(ImageName) #step4
        time.sleep(1)
        CurVolTest()             #step5
        SortData()               #step6
        LogProcess()             #step7
        time.sleep(3)
        EndTest()                #step8
    else:
        ALERT()
        messagebox.showinfo("警告","请输入合法的条码")

def TestStart():
    label_Ch1_value_CurValue['text'] = '???'
    label_Ch1_value_CurValue['bg'] = 'white'
    
    label_Ch2_value_CurValue['text'] = '???'
    label_Ch2_value_CurValue['bg'] = 'white'
    
    label_Ch3_value_CurValue['text'] = '???'
    label_Ch3_value_CurValue['bg'] = 'white'
    
    label_Ch4_value_CurValue['text'] = '???'
    label_Ch4_value_CurValue['bg'] = 'white'
    
    label_Ch5_value_CurValue['text'] = '???'
    label_Ch5_value_CurValue['bg'] = 'white'
    
    testprocess = threading.Thread(target = TestProcess)
    try:
        testprocess.start()

    except:
        print("Error: unable to start thread")
        
window = tk.Tk()
window.geometry("1320x140")
window.title('通道显示板测试')

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

#label_Ch1_title_FunctionJudge = tk.Label(labelFrame_Ch1, bg = "white", text = '功能判断：')
#label_Ch1_title_FunctionJudge.grid(row = 8, column = 0, sticky = 'wn')
#
#label_Ch1_value_SerialFUNC = tk.Label(labelFrame_Ch1, bg = "white", text = '？？？')
#label_Ch1_value_SerialFUNC.grid(row = 8, column = 1, sticky = 'wn')

label_Ch1_process = tk.Label(labelFrame_Ch1,bg = "white", text = '等待测试...')
label_Ch1_process.grid(row = 10, column = 0, sticky = 'wn')

###通道2
labelFrame_Ch2 = tk.LabelFrame(window, fg = 'blue', bg = 'white', text = "通道2")
labelFrame_Ch2.grid(row=0, column = 1)

label_Ch2_title_code = tk.Label(labelFrame_Ch2, bg = "white", text = '请输入条码：')
label_Ch2_title_code.grid(row = 0, column = 0, sticky = 'wn')

entry_Ch2 = tk.Entry(labelFrame_Ch2)
"""entry_Ch1.bind("<Return>", TestStart)"""
entry_Ch2.grid(row = 0, column = 1)

label_Ch2_title_CurValue = tk.Label(labelFrame_Ch2, bg = "white", text = '总电流值(mA)：')
label_Ch2_title_CurValue.grid(row = 2, column = 0, sticky = 'wn')

label_Ch2_value_CurValue = tk.Label(labelFrame_Ch2, bg = "white", text = '？？？')
label_Ch2_value_CurValue.grid(row = 2, column = 1, sticky = 'wn')

#label_Ch2_title_FunctionJudge = tk.Label(labelFrame_Ch2, bg = "white", text = '功能判断：')
#label_Ch2_title_FunctionJudge.grid(row = 8, column = 0, sticky = 'wn')
#
#label_Ch2_value_SerialFUNC = tk.Label(labelFrame_Ch2, bg = "white", text = '？？？')
#label_Ch2_value_SerialFUNC.grid(row = 8, column = 1, sticky = 'wn')

label_Ch2_process = tk.Label(labelFrame_Ch2,bg = "white", text = '等待测试...')
label_Ch2_process.grid(row = 10, column = 0, sticky = 'wn')

###通道3
labelFrame_Ch3 = tk.LabelFrame(window, fg = 'blue', bg = 'white', text = "通道3")
labelFrame_Ch3.grid(row=0, column = 2)

label_Ch3_title_code = tk.Label(labelFrame_Ch3, bg = "white", text = '请输入条码：')
label_Ch3_title_code.grid(row = 0, column = 0, sticky = 'wn')

entry_Ch3 = tk.Entry(labelFrame_Ch3)
"""entry_Ch1.bind("<Return>", TestStart)"""
entry_Ch3.grid(row = 0, column = 1)

label_Ch3_title_CurValue = tk.Label(labelFrame_Ch3, bg = "white", text = '总电流值(mA)：')
label_Ch3_title_CurValue.grid(row = 2, column = 0, sticky = 'wn')

label_Ch3_value_CurValue = tk.Label(labelFrame_Ch3, bg = "white", text = '？？？')
label_Ch3_value_CurValue.grid(row = 2, column = 1, sticky = 'wn')

#label_Ch3_title_FunctionJudge = tk.Label(labelFrame_Ch3, bg = "white", text = '功能判断：')
#label_Ch3_title_FunctionJudge.grid(row = 8, column = 0, sticky = 'wn')
#
#label_Ch3_value_SerialFUNC = tk.Label(labelFrame_Ch3, bg = "white", text = '？？？')
#label_Ch3_value_SerialFUNC.grid(row = 8, column = 1, sticky = 'wn')

label_Ch3_process = tk.Label(labelFrame_Ch3,bg = "white", text = '等待测试...')
label_Ch3_process.grid(row = 10, column = 0, sticky = 'wn')

###通道4
labelFrame_Ch4 = tk.LabelFrame(window, fg = 'blue', bg = 'white', text = "通道4")
labelFrame_Ch4.grid(row=0, column = 3)

label_Ch4_title_code = tk.Label(labelFrame_Ch4, bg = "white", text = '请输入条码：')
label_Ch4_title_code.grid(row = 0, column = 0, sticky = 'wn')

entry_Ch4 = tk.Entry(labelFrame_Ch4)
"""entry_Ch1.bind("<Return>", TestStart)"""
entry_Ch4.grid(row = 0, column = 1)

label_Ch4_title_CurValue = tk.Label(labelFrame_Ch4, bg = "white", text = '总电流值(mA)：')
label_Ch4_title_CurValue.grid(row = 2, column = 0, sticky = 'wn')

label_Ch4_value_CurValue = tk.Label(labelFrame_Ch4, bg = "white", text = '？？？')
label_Ch4_value_CurValue.grid(row = 2, column = 1, sticky = 'wn')

#label_Ch4_title_FunctionJudge = tk.Label(labelFrame_Ch4, bg = "white", text = '功能判断：')
#label_Ch4_title_FunctionJudge.grid(row = 8, column = 0, sticky = 'wn')
#
#label_Ch4_value_SerialFUNC = tk.Label(labelFrame_Ch4, bg = "white", text = '？？？')
#label_Ch4_value_SerialFUNC.grid(row = 8, column = 1, sticky = 'wn')

label_Ch4_process = tk.Label(labelFrame_Ch4,bg = "white", text = '等待测试...')
label_Ch4_process.grid(row = 10, column = 0, sticky = 'wn')

###通道5
labelFrame_Ch5 = tk.LabelFrame(window, fg = 'blue', bg = 'white', text = "通道5")
labelFrame_Ch5.grid(row=0, column = 4)

label_Ch5_title_code = tk.Label(labelFrame_Ch5, bg = "white", text = '请输入条码：')
label_Ch5_title_code.grid(row = 0, column = 0, sticky = 'wn')

entry_Ch5 = tk.Entry(labelFrame_Ch5)
"""entry_Ch1.bind("<Return>", TestStart)"""
entry_Ch5.grid(row = 0, column = 1)

label_Ch5_title_CurValue = tk.Label(labelFrame_Ch5, bg = "white", text = '总电流值(mA)：')
label_Ch5_title_CurValue.grid(row = 2, column = 0, sticky = 'wn')

label_Ch5_value_CurValue = tk.Label(labelFrame_Ch5, bg = "white", text = '？？？')
label_Ch5_value_CurValue.grid(row = 2, column = 1, sticky = 'wn')

#label_Ch5_title_FunctionJudge = tk.Label(labelFrame_Ch5, bg = "white", text = '功能判断：')
#label_Ch5_title_FunctionJudge.grid(row = 8, column = 0, sticky = 'wn')
#
#label_Ch5_value_SerialFUNC = tk.Label(labelFrame_Ch5, bg = "white", text = '？？？')
#label_Ch5_value_SerialFUNC.grid(row = 8, column = 1, sticky = 'wn')

label_Ch5_process = tk.Label(labelFrame_Ch5,bg = "white", text = '等待测试...')
label_Ch5_process.grid(row = 10, column = 0, sticky = 'wn')

button_start = tk.Button(window,width=32,height=3,text='开始测试',padx=1,pady=1,anchor='c',command=TestStart,)
button_start.grid(row = 1, column = 2, sticky = 'wn')

window.mainloop()
