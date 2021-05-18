import time
import tkinter as tk
import RPi.GPIO as GPIO
import MotoDirection

def ch1_test(even):
    label_ch1_result1['bg'] = 'blue'
    label_ch1_result1['text'] = '检测中...'
    label_ch1_result2['bg'] = 'blue'
    label_ch1_result2['text'] = '检测中...'
    label_ch1_result3['bg'] = 'blue'
    label_ch1_result3['text'] = '检测中...'
    label_ch1_result4['bg'] = 'blue'
    label_ch1_result4['text'] = '检测中...'
    window.update()
    MotoDirection.MotoPortInit()
    
    MotoDirection.MotoPosInit()
    time.sleep(0.5)
    MotoDirection.MotoPosDirTest(label_ch1_result1)
    window.update()
    
    MotoDirection.MotoPosInit()
    time.sleep(0.5)    
    MotoDirection.MotoNegDirTest(label_ch1_result2)
    window.update()
    
    MotoDirection.MotoPosInit()
    time.sleep(0.5)
    MotoDirection.MotoPosSpdTest(label_ch1_result3, 1600)  #800 steps/cicle
    window.update()
    
    MotoDirection.MotoPosInit()
    time.sleep(0.5)
    MotoDirection.MotoNegSpdTest(label_ch1_result4, 1600)  #800 steps/cicle
    window.update()

window = tk.Tk()
window.geometry("300x200")
window.title('电机驱动板测试')

'''''''''''''''''''''
通道1
'''''''''''''''''''''
labelFrame_ch1 = tk.LabelFrame(window, fg = 'blue', bg = 'white', text = "通道1")
labelFrame_ch1.grid(row=0, column = 0)

label_ch1_show1 = tk.Label(labelFrame_ch1, bg = "white", text = '请输入条码：')
label_ch1_show1.grid(row = 0, column = 0, sticky = 'wn')

entry_ch1 = tk.Entry(labelFrame_ch1)
entry_ch1.bind("<Return>", ch1_test)
entry_ch1.grid(row = 0, column = 1)

label_ch1_show2 = tk.Label(labelFrame_ch1, bg = "white", text = '电机正向测试：')
label_ch1_show2.grid(row = 1, column = 0, sticky = 'wn')

label_ch1_result1 = tk.Label(labelFrame_ch1, bg = "yellow", text = '待测', width = 10)
label_ch1_result1.grid(row = 1, column = 1, sticky = 'e')

label_ch1_show3 = tk.Label(labelFrame_ch1, bg = "white", text = '电机反向测试：')
label_ch1_show3.grid(row = 2, column = 0, sticky = 'wn')

label_ch1_result2 = tk.Label(labelFrame_ch1, bg = "yellow", text = '待测', width = 10)
label_ch1_result2.grid(row = 2, column = 1, sticky = 'e')

label_ch1_show4 = tk.Label(labelFrame_ch1, bg = "white", text = '电机正向速度测试：')
label_ch1_show4.grid(row = 3, column = 0, sticky = 'wn')

label_ch1_result3 = tk.Label(labelFrame_ch1, bg = "yellow", text = '待测', width = 10)
label_ch1_result3.grid(row = 3, column = 1, sticky = 'e')

label_ch1_show5 = tk.Label(labelFrame_ch1, bg = "white", text = '电机反向速度测试：')
label_ch1_show5.grid(row = 4, column = 0, sticky = 'wn')

label_ch1_result4 = tk.Label(labelFrame_ch1, bg = "yellow", text = '待测', width = 10)
label_ch1_result4.grid(row = 4, column = 1, sticky = 'e')
window.mainloop()
