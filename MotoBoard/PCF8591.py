#coding=utf-8
# _*_ coding UTF-8 _*_
import smbus
import time

bus = smbus.SMBus(1) ##开启总线 

def voltage(address,channel):
    bus.write_byte(address,channel)
    value1 = bus.read_byte(address)/256*5
    value2 = bus.read_byte(address)/256*5
    ValueAfter = round(value2,5)
    return ValueAfter
    
