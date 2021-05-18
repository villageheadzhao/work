import os
import time
from ctypes import *
 
class CH341():
     def __init__(self, dev = 0x5c):
         self.dev_addr = dev
 
     def read(self, addr, regaddr):
         ch341 = windll.LoadLibrary("CH341DLL.DLL")
         ch341.CH341OpenDevice(0)
         ch341.CH341SetStream(0, 0x82)
         obuf = (c_byte * 2)()
         ibuf = (c_byte * 2)()
         obuf[0] = self.dev_addr
         obuf[1] = addr
         ch341.CH341ReadI2C(0, addr, regaddr, ibuf)
         ch341.CH341CloseDevice(0)
         print("ibuf", ibuf[0])
         return ibuf[0] & 0xff
 
     def write(self, addr, regaddr, dat):
         ch341 = windll.LoadLibrary("CH341DLL.DLL")
         ch341.CH341OpenDevice(0)
         ch341.CH341SetStream(0, 0x82)

         ch341.CH341WriteI2C(0, addr, regaddr, dat)
         #obuf = (c_byte * 3)()
         #ibuf = (c_byte * 1)()
         #obuf[0] = self.dev_addr
         #obuf[1] = addr
         #obuf[2] = dat & 0xff
         #print("obuf[0]=",obuf[0])
         #print("obuf[1]=",obuf[1])
         #print("obuf[2]=",obuf[2])
         #ch341.CH341StreamI2C(0, 3, obuf, 0, ibuf)
         ch341.CH341CloseDevice(0)
     def flushbuffer(self):
         ch341 = windll.LoadLibrary("CH341DLL.DLL")
         ch341.CH341OpenDevice(0)
         ch341.CH341SetStream(0, 0x82)
         ch341.CH341FlushBuffer(0)
         
          
