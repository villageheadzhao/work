#coding=utf-8
#!/usr/bin/python
# _*_ coding utf-8 _*_
import os
import time
import ch341
from ctypes import *

MCP23017_IODIRA = 0x00
MCP23017_IPOLA  = 0x02
MCP23017_GPINTENA = 0x04
MCP23017_DEFVALA = 0x06
MCP23017_INTCONA = 0x08
MCP23017_IOCONA = 0x0A
MCP23017_GPPUA = 0x0C
MCP23017_INTFA = 0x0E
MCP23017_INTCAPA = 0x10
MCP23017_GPIOA = 0x12
MCP23017_OLATA = 0x14

MCP23017_IODIRB = 0x01
MCP23017_IPOLB = 0x03
MCP23017_GPINTENB = 0x05
MCP23017_DEFVALB = 0x07
MCP23017_INTCONB = 0x09
MCP23017_IOCONB = 0x0B
MCP23017_GPPUB = 0x0D
MCP23017_INTFB = 0x0F
MCP23017_INTCAPB = 0x11
MCP23017_GPIOB = 0x13
MCP23017_OLATB = 0x15

ch341 = windll.LoadLibrary("CH341DLL.DLL")
ch341.CH341OpenDevice(0)
ch341.CH341SetStream(0, 0x82)


def IOExtInit(ADDRESS):
    MCP23017_ADDRESS = ADDRESS
    #Configue the register to default value
    for addr in range(22):
        if (addr == 0) or (addr == 1):
            ch341.CH341WriteI2C(0, MCP23017_ADDRESS, addr, 0xFF)
        else:
            ch341.CH341WriteI2C(0, MCP23017_ADDRESS, addr, 0x00)


def IOExtChAWrite(ADDRESS,value):
    MCP23017_ADDRESS = ADDRESS
    #configue PinA0～7 as output        
    ch341.CH341WriteI2C(0,MCP23017_ADDRESS,MCP23017_IODIRA,0x00)
    ch341.CH341WriteI2C(0,MCP23017_ADDRESS,MCP23017_GPIOA,value)

def IOExtChARead(ADDRESS):
    MCP23017_ADDRESS = ADDRESS
    obuf = (c_byte * 2)()
    #configue PinA0～7 as input        
    ch341.CH341WriteI2C(0,MCP23017_ADDRESS,MCP23017_IODIRA,0xFF)
    #configue all PinA pullUP
    ch341.CH341WriteI2C(0,MCP23017_ADDRESS,MCP23017_GPPUB,0xFF)
    ch341.CH341ReadI2C(0,MCP23017_ADDRESS,MCP23017_GPIOA,obuf)
    return obuf[0] & 0xff

def IOExtChBWrite(ADDRESS,value):
    MCP23017_ADDRESS = ADDRESS
    #configue all PinB output
    ch.write(MCP23017_ADDRESS,MCP23017_IODIRB,0x00)
    ch.write(MCP23017_ADDRESS,MCP23017_GPIOB,value)

def IOExtChBRead(ADDRESS):
    MCP23017_ADDRESS = ADDRESS
    #configue all PinB input
    bus.write_byte_data(MCP23017_ADDRESS,MCP23017_IODIRB,0xFF)
    #configue all PinB pullUP
    bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPPUB,0xFF)
    return bus.read_byte_data(MCP23017_ADDRESS,MCP23017_GPIOB)



#IOExtInit(0x27)
#IOExtChAWrite(0x27,0x00)
'''
IOExtInit(0X27)

IOExtChAWrite(0X27,0Xff)
time.sleep(50)
a=IOExtChARead(0X27)

print(a)

'''
