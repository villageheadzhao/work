#!/usr/bin/env python
# -*- coding:utf-8 -*-
import smbus
import time

bus = smbus.SMBus(1) ##开启总线 

def voltage(address,channel):
    bus.write_byte(address,channel)
    value1 = bus.read_byte(address)/256*5.18
    value2 = bus.read_byte(address)/256*5.18
    ValueAfter = round(value2,3)
    return ValueAfter
    
