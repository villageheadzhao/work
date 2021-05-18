#coding=utf-8
import shutil
import os
from ftplib import FTP
import os
import tarfile

def LogUpload(LogName):
    ftp = FTP()
    timeout = 30
    port = 21
    ftp.connect('192.168.1.100', port, timeout)
    ftp.login('administrator', 'yakai888')
    print(ftp.getwelcome())

    #ftp.mkd("TestLog/log") #新建文件夹
    ftp.cwd("TestLog/PowerBoard")  #创建操作目录

    localpath = "/home/pi/Desktop/work/Finalversion/Moto/"
    localfile = localpath + LogName + '.csv'
    f=open(localfile,'rb')

    ftp.storbinary('STOR %s' % os.path.basename(localfile),f)
