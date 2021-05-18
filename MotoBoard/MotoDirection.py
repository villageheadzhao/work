#coding=utf-8
import time
import RPi.GPIO as GPIO
import tkinter as tk

def MotoPortInit(StepPort,EnPort,DirPort,Pos1Port,Pos2Port):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) ##GPIO.BCM
    GPIO.setup(StepPort,GPIO.OUT)  ##SM_STEP
    GPIO.setup(EnPort,GPIO.OUT)  ##SM_EN
    GPIO.setup(DirPort,GPIO.OUT)  ##SM_DIR
    GPIO.setup(Pos1Port,GPIO.IN)  ##MOTPOS1
    GPIO.setup(Pos2Port,GPIO.IN)  ##MOTPOS2
    GPIO.output(EnPort,GPIO.LOW)

def MotoPosInit(StepPort,DirPort,Pos1Port,Pos2Port,labelx):
    GPIO.output(DirPort,GPIO.HIGH)
    p = GPIO.PWM(StepPort, 100)  #(CHANEL, FREQ)
    p.start(15)   #(DUTY)
    time.sleep(0.1)
#    # print("Pos2PortPos2PortPos2Port-START ",GPIO.input(Pos2Port))
#    ss = GPIO.wait_for_edge(Pos2Port, GPIO.RISING, timeout = 10000)
#    # print("Pos2PortPos2PortPos2Port-END ",GPIO.input(Pos2Port))
    # print("Pos1PortPos1PortPos1Port-START ",GPIO.input(Pos1Port))
    s = GPIO.wait_for_edge(Pos1Port, GPIO.FALLING, timeout = 10000)
    # print("Pos1PortPos1PortPos1Port-END ",GPIO.input(Pos1Port))

    if s is not None:
        while True:

            value1 = GPIO.input(Pos1Port)
            value2 = GPIO.input(Pos2Port)
            #time.sleep(0.0005)
            value3 = GPIO.input(Pos1Port)
            value4 = GPIO.input(Pos2Port)
            ## print("Pos1Port ",GPIO.input(Pos1Port))
           # # print("Pos2Port ",GPIO.input(Pos2Port))
            if(value1 == 0 and value2 == 0 and value3 == 0 and value4 == 0):
            #if(value1 == 0 and value2 == 0):
                p.stop()
                value5 = GPIO.input(Pos1Port)
                value6= GPIO.input(Pos2Port)
                # print("value5******",value5)
                # print("value6******",value6)
                if(value5 ==1 or value6 ==1):
                    MotoPosInit(StepPort,DirPort,Pos1Port,Pos2Port,labelx)
                    break
                break
    else:
        labelx['text'] = "FAIL"
        labelx['bg'] = "red"


def MotoPosInit_NEGDIR(StepPort,DirPort,Pos1Port,Pos2Port,labelx):
    GPIO.output(DirPort,GPIO.LOW)
    p = GPIO.PWM(StepPort, 100)  #(CHANEL, FREQ)
    p.start(15)   #(DUTY)
    time.sleep(0.1)
#    # print("Pos2PortPos2PortPos2Port-START ",GPIO.input(Pos2Port))
#    ss = GPIO.wait_for_edge(Pos2Port, GPIO.RISING, timeout = 10000)
#    # print("Pos2PortPos2PortPos2Port-END ",GPIO.input(Pos2Port))
    # print("Pos1PortPos1PortPos1Port-START ",GPIO.input(Pos1Port))
    s = GPIO.wait_for_edge(Pos2Port, GPIO.FALLING, timeout = 10000)
    # print("Pos1PortPos1PortPos1Port-END ",GPIO.input(Pos1Port))

    if s is not None:
        while True:

            value1 = GPIO.input(Pos1Port)
            value2 = GPIO.input(Pos2Port)
            #time.sleep(0.0005)
            value3 = GPIO.input(Pos1Port)
            value4 = GPIO.input(Pos2Port)
           # # print("Pos1Port ",GPIO.input(Pos1Port))
           ## print("Pos2Port ",GPIO.input(Pos2Port))
            if(value1 == 0 and value2 == 0 and value3 == 0 and value4 == 0):
            #if(value1 == 0 and value2 == 0):
                p.stop()
                value5 = GPIO.input(Pos1Port)
                value6= GPIO.input(Pos2Port)
                # print("value5******",value5)
                # print("value6******",value6)
                if(value5 ==1 or value6 ==1):
                    MotoPosInit_NEGDIR(StepPort,DirPort,Pos1Port,Pos2Port,labelx)
                    break
                break
    else:
        labelx['text'] = "FAIL"
        labelx['bg'] = "red"

def MotoPosDirTest(StepPort,DirPort,Pos1Port,Pos2Port,labelx):
    value7 = GPIO.input(Pos1Port)
    value8= GPIO.input(Pos2Port)
    # print("value7$$$$$$$",value7)
    # print("value8$$$$$$$",value8)
    if(value7 == 1 or value8 == 1):
        MotoPosInit(StepPort,DirPort,Pos1Port,Pos2Port,labelx)
        GPIO.output(DirPort,GPIO.HIGH)
        p = GPIO.PWM(StepPort, 100)  #(CHANEL, FREQ)
        p.start(15)   #(DUTY)
#        time.sleep(0.01)
        # print('pos test if')

        s1 = GPIO.wait_for_edge(Pos2Port, GPIO.RISING, timeout = 10000)

        time.sleep(0.02)

        p.stop()

        if s1 is not None:
            #p.stop()
            time.sleep(1)
            # print("Pos1Port++++++++++++++++++++",GPIO.input(Pos1Port))
            # print("Pos2Port++++++++++++++++++++",GPIO.input(Pos2Port))
            while True:
                if(GPIO.input(Pos1Port) == 0 and GPIO.input(Pos2Port) == 1):
                    time.sleep(0.1)
                    # print("right")
                    # print("Pos1Port++++++++++++++++++++",GPIO.input(Pos1Port))
                    # print("Pos2Port++++++++++++++++++++",GPIO.input(Pos2Port))
    #                p.stop()
                    labelx['text'] = "PASS"
                    labelx['bg'] = "green"
                    TestResult=1
                    break
                if(GPIO.input(Pos1Port) == 1 and GPIO.input(Pos2Port) == 0):
                    time.sleep(0.1)
                    # print("wrong10")
                    # print("Pos1Port++++++++++++++++++++",GPIO.input(Pos1Port))
                    # print("Pos2Port++++++++++++++++++++",GPIO.input(Pos2Port))
    #                p.stop()
                    labelx['text'] = "FAIL"
                    labelx['bg'] = "red"
                    TestResult=0
                    break
                if(GPIO.input(Pos1Port) == 1 and GPIO.input(Pos2Port) == 1):
                    time.sleep(0.1)
                    # print("wrong11")
                    # print("Pos1Port++++++++++++++++++++",GPIO.input(Pos1Port))
                    # print("Pos2Port++++++++++++++++++++",GPIO.input(Pos2Port))
    #                p.stop()
                    labelx['text'] = "FAIL"
                    labelx['bg'] = "red"
                    TestResult=0
                    break
                if(GPIO.input(Pos1Port) == 0 and GPIO.input(Pos2Port) == 0):
                    time.sleep(0.1)
                    # print("wrong00")
                    # print("Pos1Port++++++++++++++++++++",GPIO.input(Pos1Port))
                    # print("Pos2Port++++++++++++++++++++",GPIO.input(Pos2Port))
    #                p.stop()
                    labelx['text'] = "FAIL"
                    labelx['bg'] = "red"
                    TestResult=0
                    break
        else:
            labelx['text'] = "FAIL"
            labelx['bg'] = "red"

    else:
        GPIO.output(DirPort,GPIO.HIGH)
        p = GPIO.PWM(StepPort, 100)  #(CHANEL, FREQ)
        p.start(15)   #(DUTY)
#        time.sleep(0.01)
        # print('pos test else')

        s1 = GPIO.wait_for_edge(Pos2Port, GPIO.RISING, timeout = 10000)

        time.sleep(0.02)

        p.stop()

        if s1 is not None:
            #p.stop()
            time.sleep(1)
            # print("Pos1Port++++++++++++++++++++",GPIO.input(Pos1Port))
            # print("Pos2Port++++++++++++++++++++",GPIO.input(Pos2Port))
            while True:
                if(GPIO.input(Pos1Port) == 0 and GPIO.input(Pos2Port) == 1):
                    time.sleep(0.1)
                    # print("right")
                    # print("Pos1Port++++++++++++++++++++",GPIO.input(Pos1Port))
                    # print("Pos2Port++++++++++++++++++++",GPIO.input(Pos2Port))
    #                p.stop()
                    labelx['text'] = "PASS"
                    labelx['bg'] = "green"
                    TestResult=1
                    break
                if(GPIO.input(Pos1Port) == 1 and GPIO.input(Pos2Port) == 0):
                    time.sleep(0.1)
                    # print("wrong10")
                    # print("Pos1Port++++++++++++++++++++",GPIO.input(Pos1Port))
                    # print("Pos2Port++++++++++++++++++++",GPIO.input(Pos2Port))
    #                p.stop()
                    labelx['text'] = "FAIL"
                    labelx['bg'] = "red"
                    TestResult=0
                    break
                if(GPIO.input(Pos1Port) == 1 and GPIO.input(Pos2Port) == 1):
                    time.sleep(0.1)
                    # print("wrong11")
                    # print("Pos1Port++++++++++++++++++++",GPIO.input(Pos1Port))
                    # print("Pos2Port++++++++++++++++++++",GPIO.input(Pos2Port))
    #                p.stop()
                    labelx['text'] = "FAIL"
                    labelx['bg'] = "red"
                    TestResult=0
                    break
                if(GPIO.input(Pos1Port) == 0 and GPIO.input(Pos2Port) == 0):
                    time.sleep(0.1)
                    # print("wrong00")
                    # print("Pos1Port++++++++++++++++++++",GPIO.input(Pos1Port))
                    # print("Pos2Port++++++++++++++++++++",GPIO.input(Pos2Port))
    #                p.stop()
                    labelx['text'] = "FAIL"
                    labelx['bg'] = "red"
                    TestResult=0
                    break
        else:
            labelx['text'] = "FAIL"
            labelx['bg'] = "red"


def MotoNegDirTest(StepPort,DirPort,Pos1Port,Pos2Port,labelx):
    value9 = GPIO.input(Pos1Port)
    value0= GPIO.input(Pos2Port)
    # print("value9$$$$$$$",value9)
    # print("value0$$$$$$$",value0)
    if(value9 == 1 or value0 == 1):
        MotoPosInit_NEGDIR(StepPort,DirPort,Pos1Port,Pos2Port,labelx)
        GPIO.output(DirPort,GPIO.LOW)
        p = GPIO.PWM(StepPort, 100)  #(CHANEL, FREQ)
        p.start(15)   #(DUTY)

        # print('neg test if')
#        time.sleep(0.01)
        s2 = GPIO.wait_for_edge(Pos1Port, GPIO.RISING, timeout = 10000)

        time.sleep(0.02)

        p.stop()

        if s2 is not None:
            #p.stop()
            time.sleep(1)
            # print("Pos1Port-------------------",GPIO.input(Pos1Port))
            # print("Pos2Port-------------------",GPIO.input(Pos2Port))
            while True:
                if(GPIO.input(Pos1Port) == 1 and GPIO.input(Pos2Port) == 0):
                    time.sleep(0.1)
                    # print("right")
                    # print("Pos1Port-------------------",GPIO.input(Pos1Port))
                    # print("Pos2Port-------------------",GPIO.input(Pos2Port))
                    labelx['text'] = "PASS"
                    labelx['bg'] = "green"
                    TestResult=1
                    break
                if(GPIO.input(Pos1Port) == 0 and GPIO.input(Pos2Port) == 1):
                    time.sleep(0.1)
                    # print("wrong10")
                    # print("Pos1Port-------------------",GPIO.input(Pos1Port))
                    # print("Pos2Port-------------------",GPIO.input(Pos2Port))
                    labelx['text'] = "FAIL"
                    labelx['bg'] = "red"
                    TestResult=0
                    break
                if(GPIO.input(Pos1Port) == 1 and GPIO.input(Pos2Port) == 1):
                    time.sleep(0.1)
                    # print("wrong11")
                    # print("Pos1Port-------------------",GPIO.input(Pos1Port))
                    # print("Pos2Port-------------------",GPIO.input(Pos2Port))
                    labelx['text'] = "FAIL"
                    labelx['bg'] = "red"
                    TestResult=0
                    break
                if(GPIO.input(Pos1Port) == 0 and GPIO.input(Pos2Port) == 0):
                    time.sleep(0.1)
                    # print("wrong00")
                    # print("Pos1Port-------------------",GPIO.input(Pos1Port))
                    # print("Pos2Port-------------------",GPIO.input(Pos2Port))
                    labelx['text'] = "FAIL"
                    labelx['bg'] = "red"
                    TestResult=0
                    break
        else:
            labelx['text'] = "FAIL"
            labelx['bg'] = "red"

    else:
        GPIO.output(DirPort,GPIO.LOW)
        p = GPIO.PWM(StepPort, 100)  #(CHANEL, FREQ)
        p.start(15)   #(DUTY)

        # print('neg test else')
#        time.sleep(0.01)
        s2 = GPIO.wait_for_edge(Pos1Port, GPIO.RISING, timeout = 10000)

        time.sleep(0.02)

        p.stop()

        if s2 is not None:
            #p.stop()
            time.sleep(1)
            # print("Pos1Port-------------------",GPIO.input(Pos1Port))
            # print("Pos2Port-------------------",GPIO.input(Pos2Port))
            while True:
                if(GPIO.input(Pos1Port) == 1 and GPIO.input(Pos2Port) == 0):
                    time.sleep(0.1)
                    # print("right")
                    # print("Pos1Port-------------------",GPIO.input(Pos1Port))
                    # print("Pos2Port-------------------",GPIO.input(Pos2Port))
                    labelx['text'] = "PASS"
                    labelx['bg'] = "green"
                    TestResult=1
                    break
                if(GPIO.input(Pos1Port) == 0 and GPIO.input(Pos2Port) == 1):
                    time.sleep(0.1)
                    # print("wrong10")
                    # print("Pos1Port-------------------",GPIO.input(Pos1Port))
                    # print("Pos2Port-------------------",GPIO.input(Pos2Port))
                    labelx['text'] = "FAIL"
                    labelx['bg'] = "red"
                    TestResult=0
                    break
                if(GPIO.input(Pos1Port) == 1 and GPIO.input(Pos2Port) == 1):
                    time.sleep(0.1)
                    # print("wrong11")
                    # print("Pos1Port-------------------",GPIO.input(Pos1Port))
                    # print("Pos2Port-------------------",GPIO.input(Pos2Port))
                    labelx['text'] = "FAIL"
                    labelx['bg'] = "red"
                    TestResult=0
                    break
                if(GPIO.input(Pos1Port) == 0 and GPIO.input(Pos2Port) == 0):
                    time.sleep(0.1)
                    # print("wrong00")
                    # print("Pos1Port-------------------",GPIO.input(Pos1Port))
                    # print("Pos2Port-------------------",GPIO.input(Pos2Port))
                    labelx['text'] = "FAIL"
                    labelx['bg'] = "red"
                    TestResult=0
                    break
        else:
            labelx['text'] = "FAIL"
            labelx['bg'] = "red"


def MotoPosSpdTest(StepPort,DirPort,Pos1Port,Pos2Port,labelx, steps):
    value11 = GPIO.input(Pos1Port)
    value12= GPIO.input(Pos2Port)
    # print("value11$$$$$$$",value11)
    # print("value12$$$$$$$",value12)
    GPIO.remove_event_detect(Pos2Port)
#    GPIO.remove_event_detect(Pos1Port)
    GPIO.add_event_detect(Pos2Port, GPIO.RISING, bouncetime = 80)
    #GPIO.add_event_detect(Pos1Port, GPIO.FALLING)
    if(value11 == 1 or value12 == 1):
        MotoPosInit(StepPort,DirPort,Pos1Port,Pos2Port,labelx)
        GPIO.output(DirPort,GPIO.HIGH)
        OptoValueCurrent = 2
        num = 0

        for i in range(steps):
            time.sleep(0.0006)
            GPIO.output(StepPort,GPIO.HIGH)
            time.sleep(0.0006) #0.001
            GPIO.output(StepPort,GPIO.LOW)

#            time.sleep(0.0001)
#            OptoValuePrevious =  OptoValueCurrent

            if GPIO.event_detected(Pos2Port):
               # # print("GPIO.event_detected(Pos2Port)##### ",GPIO.event_detected(Pos2Port))

                num += 1
        num = num - 1
        if num == 12:
            labelx['text'] = "PASS"
            labelx['bg'] = "green"
            # print(num)
            num = 0
            TestResult=1
        else:
            labelx['text'] = "FAIL"
            labelx['bg'] = "red"
            # print(num)
            num = 0
            TestResult=0
        return TestResult
    else:
        GPIO.output(DirPort,GPIO.HIGH)
        OptoValueCurrent = 2
        num = 0

        for i in range(steps):
            time.sleep(0.0006)
            GPIO.output(StepPort,GPIO.HIGH)
            time.sleep(0.0006) #0.001
            GPIO.output(StepPort,GPIO.LOW)

#            time.sleep(0.0001)
#            OptoValuePrevious =  OptoValueCurrent

            if GPIO.event_detected(Pos2Port):
                ## print("GPIO.event_detected(Pos2Port)##### ",GPIO.event_detected(Pos2Port))

                num += 1

        if num == 12:
            labelx['text'] = "PASS"
            labelx['bg'] = "green"
            # print(num)
            num = 0
            TestResult=1
        else:
            labelx['text'] = "FAIL"
            labelx['bg'] = "red"
            # print(num)
            num = 0
            TestResult=0
        return TestResult


def MotoNegSpdTest(StepPort,DirPort,Pos1Port,Pos2Port,labelx, steps):
    value13 = GPIO.input(Pos1Port)
    value14= GPIO.input(Pos2Port)
    # print("value13$$$$$$$",value13)
    # print("value14$$$$$$$",value14)
    GPIO.remove_event_detect(Pos1Port)
    GPIO.add_event_detect(Pos1Port, GPIO.RISING, bouncetime = 80)
    if(value13 == 1 or value14 == 1):
        MotoPosInit_NEGDIR(StepPort,DirPort,Pos1Port,Pos2Port,labelx)
        GPIO.output(DirPort,GPIO.LOW)
        OptoValueCurrent = 2
        num = 0
        for i in range(steps):
            time.sleep(0.0006)
            GPIO.output(StepPort,GPIO.HIGH)
            time.sleep(0.0006)
            GPIO.output(StepPort,GPIO.LOW)
#            time.sleep(0.0001)

            if GPIO.event_detected(Pos1Port):
                num += 1
        num = num - 1
        if num == 12:
            labelx['text'] = "PASS"
            labelx['bg'] = "green"
            # print(num)
            num = 0
            TestResult=1
        else:
            labelx['text'] = "FAIL"
            labelx['bg'] = "red"
            # print(num)
            num = 0
            TestResult=0
        return TestResult
    else:
        GPIO.output(DirPort,GPIO.LOW)
        OptoValueCurrent = 2
        num = 0
        for i in range(steps):
            time.sleep(0.0006)
            GPIO.output(StepPort,GPIO.HIGH)
            time.sleep(0.0006)
            GPIO.output(StepPort,GPIO.LOW)
#            time.sleep(0.0001)

            if GPIO.event_detected(Pos1Port):
                num += 1
        if num == 12:
            labelx['text'] = "PASS"
            labelx['bg'] = "green"
            # print(num)
            num = 0
            TestResult=1
        else:
            labelx['text'] = "FAIL"
            labelx['bg'] = "red"
            # print(num)
            num = 0
            TestResult=0
        return TestResult


def MotoRun(StepPort,DirPort,Switch):   #switch=1: 起动电机 switch=0: 关闭电机
    MotoPortInit()
    GPIO.output(DirPort,GPIO.HIGH)
    p = GPIO.PWM(StepPort, 1000)  #(CHANEL, FREQ)
    #if Switch == 1:
    p.start(15)   #(DUTY)
    #else:
        #p.stop()
