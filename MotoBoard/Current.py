#coding=utf-8
import time
import serial

def CurrentRead(portx):

    ser = serial.Serial(portx,9600)
    ser.close()
    ser.open()
    ser.flushInput()
    ser.write("AT+C\r\n".encode("utf-8"))
    time.sleep(0.1)
    count = ser.inWaiting()
    recv = (ser.read(count)).decode("utf-8")
    ser.close()
    Current_Read = float(recv[3:8])*1000

    return Current_Read

