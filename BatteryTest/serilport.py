# coding=utf-8
# encoding: utf-8
import time
import serial
from binascii import *


# 打开串口
def sourceserialopen(portx):
    ser = serial.Serial(portx, 115200)
    ser.close()
    time.sleep(0.5)
    ser.open()


# 关闭串口
def sourceserialclose(portx):
    ser = serial.Serial(portx, 115200)
    ser.close()
    time.sleep(0.5)


def start(portx, address):
    global start_signal
    i = 0
    start_signal = True
    ser = serial.Serial(portx, 115200)
    ser.flushInput()
    startcommend = bytes.fromhex(address)
    ser.write(startcommend)
    while start_signal:
        count = ser.inWaiting()
        if count > 6:
            start_signal = False
            return
        else:
            i = i + 1
            print("i", i)
            if i > 20:
                start_signal = False
                teststate = "FF"
                return teststate
            else:
                start_signal = True


# 停止
def stop(portx, address):
    global stop_signal
    i = 0
    stop_signal = True
    ser = serial.Serial(portx, 115200)
    ser.flushInput()
    stopcommend = bytes.fromhex(address)
    ser.write(stopcommend)
    while stop_signal:
        count = ser.inWaiting()
        if count > 6:
            # print(count)
            stop_signal = False
            return
        else:
            i = i + 1
            if i > 20:
                stop_signal = False
                stop_value = "FF"
                return stop_value
            else:
                stop_signal = True


#读取数据
def readdata(portx, address):
    global read_signal
    read_signal = True
    i = 0
    ser = serial.Serial(portx, 115200)
    ser.flushInput()
    readdatacommend = bytes.fromhex(address)
    ser.write(readdatacommend)

    while read_signal:
        count = ser.inWaiting()
        if count > 122:
            recv = ser.read(count)
            # x = hex(recv[3])[2:]
            #y = hex(recv[4])[2:]
            #data = x + y
            teststate = recv
            # print("串口数据", teststate)
            read_signal = False
            return teststate
        else:
            i = i + 1
            #print("i", i)
            if i > 6000:
                read_signal = False
                teststate = "FF"
                return teststate
            else:
                read_signal = True


def readenvironmenttemperature(portx):
    global environment_signal
    environment_signal = True
    i = 0
    ser = serial.Serial(portx, 9600)
    ser.flushInput()
    readenvironmenttemperaturecommend = bytes.fromhex("010300200002C5C1")
    ser.write(readenvironmenttemperaturecommend)

    while environment_signal:
        count = ser.inWaiting()
        if count > 6:
            # print(count)
            recv = ser.read(count)
            # print('environmenttemperature', recv)
            data = float(recv[3] << 8 | recv[4]) / 10
            environmenttemperature = data
            # print("environmenttemperature_result", environmenttemperature)
            environment_signal = False
            return environmenttemperature
        else:
            i = i + 1
            if i > 20:
                environment_signal = False
                environmenttemperature = "FF"
                return environmenttemperature
            else:
                environment_signal = True
