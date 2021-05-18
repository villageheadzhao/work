# -*- coding:utf-8 -*-
import os
import sys


def Camera(Number):
    
    PartNo = Number
    cmd = "fswebcam -S 10 -r 1024x768 /home/pi/Desktop/test/"+PartNo+".jpg"

    os.system(cmd)
