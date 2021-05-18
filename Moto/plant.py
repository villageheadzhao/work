# coding=utf-8
# encoding: utf-8
import csv
from matplotlib import pyplot as plt
from datetime import datetime
from matplotlib.font_manager import FontProperties
import pandas as pd

font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)


def quchong(logname):
    d1 = r'C:\Users\17551\Desktop\moto'
    filename = d1 + '\\' + logname + '扭矩与制动器' + '.csv'
    handle_filename = d1 + '\\' + logname + '扭矩与制动器处理后数据' + '.csv'
    # df = pd.read_csv(filename, header=0, encoding="ISO-8859-1")
    df = csv.reader(open(filename), delimiter=',')

    sortedlist = sorted(df, key=lambda x: x[3], reverse=True)
    print(sortedlist)
    with open(handle_filename, "w", newline='') as f:
        fileWriter = csv.writer(f, delimiter=',')
        for row in sortedlist:
            print(row)
            fileWriter.writerow(row)
    f.close()

    df2 = csv.reader(open(handle_filename), delimiter=',')
    sortedlist = sorted(df2, key=lambda x: x[4], reverse=True)
    print(sortedlist)
    with open(handle_filename, "w", newline='') as f:
        fileWriter = csv.writer(f, delimiter=',')
        for row in sortedlist:
            print(row)
            fileWriter.writerow(row)
    f.close()

    df1 = pd.read_csv(handle_filename, header=0, encoding="ISO-8859-1")
    datalist = df1.drop_duplicates(subset=['speed'], keep='first')
    datalist.to_csv(handle_filename, index=0)
    df1 = pd.read_csv(handle_filename, header=0, encoding="ISO-8859-1")
    datalist = df1.drop_duplicates(subset=['speed'], keep='last')
    datalist.to_csv(handle_filename, index=0)

    print('完成去重')


def dataanalysis(logname):

    quchong(logname)

    d1 = r'C:\Users\17551\Desktop\moto'
    filename = d1 + '\\' + logname + '扭矩与制动器' + '.csv'
    handle_filename = d1 + '\\' + logname + '扭矩与制动器处理后数据' + '.csv'
    with open(handle_filename) as f:  # 打开这个文件，并将结果文件对象存储在f中
        reader = csv.reader(f)  # 创建一个阅读器reader

        header_row = next(reader)  # 返回文件中的下一行
        highs, lows = [], []  # 声明存储日期，最值的列表
        print(header_row)
        for row in reader:
            high = float(row[4])  # 将字符串转换为数字
            highs.append(high)  # 存储温度最大值
            low = float(row[3])
            lows.append(low)  # 存储温度最小值

    # 根据数据绘制图形
    fig = plt.figure(dpi=128, figsize=(10, 6))
    plt.plot(highs, lows, linestyle="--", marker="*")  # 实参alpha指定颜色的透明度，0表示完全透明，1（默认值）完全不透明
    plt.xlabel('转速(RPM)', fontproperties=font_set)
    plt.ylabel("扭矩值(Nm)", fontproperties=font_set)

    plt.savefig('./'+logname + '扭矩与制动器' + '.png')
    plt.show()


def dataanalysis1(logname):
    d1 = r'C:\Users\17551\Desktop\moto'
    filename = d1 + '\\' + logname + '扭矩与转速' + '.csv'
    with open(filename) as f:  # 打开这个文件，并将结果文件对象存储在f中
        reader = csv.reader(f)  # 创建一个阅读器reader
        header_row = next(reader)  # 返回文件中的下一行
        highs, lows = [], []  # 声明存储日期，最值的列表
        print(header_row)
        for row in reader:
            high = float(row[4])  # 将字符串转换为数字
            highs.append(high)  # 存储温度最大值
            low = float(row[3])
            lows.append(low)  # 存储温度最小值

    # 根据数据绘制图形
    fig = plt.figure(dpi=128, figsize=(10, 6))
    plt.plot(highs, lows, linestyle="--", marker="*")  # 实参alpha指定颜色的透明度，0表示完全透明，1（默认值）完全不透明
    plt.xlabel(u'转速(RPM)', fontproperties=font_set)
    plt.ylabel(u"扭矩值(Nm)", fontproperties=font_set)

    plt.show()

