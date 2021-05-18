# coding=utf-8
# encoding: utf-8
import time
import serial
from binascii import *
from crcmod import *

ntc_signal = ""


# CRC16-MODBUS
def crc16add(read):
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    print(read)
    data = read.replace(" ", "")
    print('data=', data)
    readcrcout = hex(crc16(unhexlify(data))).upper()
    str_list = list(readcrcout)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0
    crc_data = "".join(str_list)
    print(crc_data)
    read = read.strip() + crc_data[4:] + crc_data[2:4]
    print('CRC16校验:', crc_data[4:] + ' ' + crc_data[2:4])
    print('增加Modbus CRC16校验：>>>', read)
    return read


# 打开串口
def sourceserialopen(portx):
    ser = serial.Serial(portx, 9600)
    ser.close()
    time.sleep(0.5)
    ser.open()


# 关闭串口
def sourceserialclose(portx):
    ser = serial.Serial(portx, 9600)
    ser.close()
    time.sleep(0.5)


# 正向启动
def forwardstart(portx, address):
    global start_signal
    start_signal = True
    ser = serial.Serial(portx, 9600)
    ser.flushInput()
    forwardstartcommend = bytes.fromhex(address)
    ser.write(forwardstartcommend)
    while start_signal:
        count = ser.inWaiting()
        if count > 6:
            print(count)
            start_signal = False
            return
        else:
            start_signal = True


# 正向停止
def forwardstop(portx, address):
    global start_signal
    start_signal = True
    ser = serial.Serial(portx, 9600)
    ser.flushInput()
    forwardstopcommend = bytes.fromhex(address)
    ser.write(forwardstopcommend)
    while start_signal:
        count = ser.inWaiting()
        if count > 6:
            print(count)
            start_signal = False
            return
        else:
            start_signal = True


# 反向启动
def reversestart(portx, address):
    global start_signal
    start_signal = True
    ser = serial.Serial(portx, 9600)
    ser.flushInput()
    reversestartcommend = bytes.fromhex(address)
    ser.write(reversestartcommend)
    while start_signal:
        count = ser.inWaiting()
        if count > 6:
            print(count)
            start_signal = False
            return
        else:
            start_signal = True


# 反向停止
def reversestop(portx, address):
    global start_signal
    start_signal = True
    ser = serial.Serial(portx, 9600)
    ser.flushInput()
    reversestopcommend = bytes.fromhex(address)
    ser.write(reversestopcommend)
    while start_signal:
        count = ser.inWaiting()
        if count > 6:
            print(count)
            start_signal = False
            return
        else:
            start_signal = True


# 步距角设置
def setstepangle(portx, address):
    global start_signal
    start_signal = True
    step_angle = address
    data = hex(int(float(step_angle) * 100))[2:].upper()
    if len(data) == 3:
        data = "0" + data
    elif len(data) == 2:
        data = "00" + data
    elif len(data) == 1:
        data = "000" + data
    else:
        data = data
    print("datadata==", data)
    step_angle_hex = "01060000" + data
    step_angle_hex_crc16 = crc16add(step_angle_hex)

    ser = serial.Serial(portx, 9600)
    ser.flushInput()
    stepanglecommend = bytes.fromhex(step_angle_hex_crc16)
    ser.write(stepanglecommend)
    while start_signal:
        count = ser.inWaiting()
        if count > 6:
            print(count)
            start_signal = False
            return
        else:
            start_signal = True


# 细分设置
def setsubdivision(portx, address):
    #step_angle = entry_ch1_1_step_angle_value.get()
    global start_signal
    start_signal = True
    subdivision = address
    data = hex(int(float(subdivision)))[2:].upper()
    if len(data) == 3:
        data = "0" + data
    elif len(data) == 2:
        data = "00" + data
    elif len(data) == 1:
        data = "000" + data
    else:
        data = data
    print("datadata==", data)
    subdivision_hex = "01060001" + data
    subdivision_hex_crc16 = crc16add(subdivision_hex)

    ser = serial.Serial(portx, 9600)
    ser.flushInput()
    subdivisioncommend = bytes.fromhex(subdivision_hex_crc16)
    ser.write(subdivisioncommend)
    while start_signal:
        count = ser.inWaiting()
        if count > 6:
            print(count)
            start_signal = False
            return
        else:
            start_signal = True


# 速度设置
def setspeed(portx, address):
    #step_angle = entry_ch1_1_step_angle_value.get()
    global start_signal
    start_signal = True
    speed = address
    data = hex(int(float(speed)))[2:].upper()
    if len(data) == 3:
        data = "0" + data
    elif len(data) == 2:
        data = "00" + data
    elif len(data) == 1:
        data = "000" + data
    else:
        data = data
    print("datadata==", data)
    speed_hex = "01060008" + data
    speed_hex_crc16 = crc16add(speed_hex)

    ser = serial.Serial(portx, 9600)
    ser.flushInput()
    speedcommend = bytes.fromhex(speed_hex_crc16)
    ser.write(speedcommend)
    while start_signal:
        count = ser.inWaiting()
        if count > 6:
            print(count)
            start_signal = False
            return
        else:
            start_signal = True


# 扭矩读取
def readtorque(portx):
    i = 0
    global torque_signal
    torque_signal = True
    ser = serial.Serial(portx, 9600)
    ser.flushInput()
    torquecommend = bytes.fromhex("010300000002C40B")
    ser.write(torquecommend)
    time.sleep(0.1)
    while torque_signal:
        count = ser.inWaiting()
        if count > 8:
            print(count)
            recv = ser.read(count)
            print(recv)
            d1 = str(hex(recv[3])[2:])
            d2 = str(hex(recv[4])[2:])
            d3 = str(hex(recv[5])[2:])
            d4 = str(hex(recv[6])[2:])
            if len(d1) == 1:
                d1 = "0" + d1
            else:
                d1 = d1

            if len(d2) == 1:
                d2 = "0" + d2
            else:
                d2 = d2

            if len(d3) == 1:
                d3 = "0" + d3
            else:
                d3 = d3

            if len(d4) == 1:
                d4 = "0" + d4
            else:
                d4 = d4

            data = d1 + d2 + d3 + d4
            data_value = int(data, 16)
            torque_signal = False
            print("****************************************************************")
            return data_value/1000
        else:
            torque_signal = True
            print("扭矩count***********", count)
            print("正在读取数值")
            i = i + 1
            if i > 10:
                torque_signal = False
                return 0
            else:
                torque_signal = True


# 转速读取
def readspeed(portx):
    global speed_signal
    i = 0
    speed_signal = True
    ser = serial.Serial(portx, 9600)
    ser.flushInput()
    speedcommend = bytes.fromhex("01030002000265CB")
    ser.write(speedcommend)
    time.sleep(0.1)
    while speed_signal:
        count = ser.inWaiting()
        if count > 8:
            print(count)
            recv = ser.read(count)
            d1 = str(hex(recv[3])[2:])
            d2 = str(hex(recv[4])[2:])
            d3 = str(hex(recv[5])[2:])
            d4 = str(hex(recv[6])[2:])
            if len(d1) == 1:
                d1 = "0" + d1
            else:
                d1 = d1

            if len(d2) == 1:
                d2 = "0" + d2
            else:
                d2 = d2

            if len(d3) == 1:
                d3 = "0" + d3
            else:
                d3 = d3

            if len(d4) == 1:
                d4 = "0" + d4
            else:
                d4 = d4

            data = d1 + d2 + d3 + d4
            data_value = int(data, 16)
            speed_signal = False
            return data_value
        else:
            speed_signal = True
            print("转速count", count)
            print("正在读取数值")
            i = i + 1
            if i > 10:
                speed_signal = False
                return 0
            else:
                speed_signal = True


# 磁粉制动器设置
def setbrake(portx, address):
    global brake_signal
    brake_signal = True
    brake = address
    data = hex(int(float(brake) * 100))[2:].upper()
    if len(data) == 3:
        data = "0" + data
    elif len(data) == 2:
        data = "00" + data
    elif len(data) == 1:
        data = "000" + data
    else:
        data = data
    print("datadata==", data)
    brake_hex = "FE060000" + data
    brake_hex_crc16 = crc16add(brake_hex)

    ser = serial.Serial(portx, 9600)
    ser.flushInput()
    brakecommend = bytes.fromhex(brake_hex_crc16)
    ser.write(brakecommend)
    while brake_signal:
        count = ser.inWaiting()
        if count > 6:
            print(count)
            brake_signal = False
            print("start_signal", brake_signal)
            ser.close()
            return 1
        else:
            brake_signal = True

'''
com = "COM11"
forward_start_commend = "01050004FF00"
forward_stop_commend = "010500040000"
setspeed(com, "100")
start_commend_crc16 = crc16add(forward_start_commend)
stop_commend_crc16 = crc16add(forward_stop_commend)
forwardstart(com, start_commend_crc16)
time.sleep(3)
forwardstop(com, stop_commend_crc16)
#setstepangle(com, "1.8")
'''
