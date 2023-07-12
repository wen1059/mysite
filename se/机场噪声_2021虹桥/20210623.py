import math
import os
import re
import pymysql
import xlwings
import time
import shutil
import traceback
from decimal import Decimal
import csv


def yieldsht(walkpath):
    """
    生成每个要处理的表
    :return:
    """
    app_24 = xlwings.App(visible=False, add_book=False)  # 待计算文件
    for root, _, files in os.walk(walkpath):
        for filexlsx in files:
            # if filexlsx[-5:-1] != '.xls' or '~$' in filexlsx:
            if ('.xls' not in filexlsx) or '~$' in filexlsx:
                continue
            file24path = os.path.join(root, filexlsx)
            file24 = app_24.books.open(file24path)  # 24小时文件
            # shtcount = file24.sheets.count  # sheet数量
            # for sc in range(shtcount):
            #     sht = file24.sheets[sc]  # sht：其中一天的sheet
            yield file24.name, file24.sheets[0]
            file24.close()
    app_24.quit()


def count_hb(sht):
    """
    统计3个时间段航班数，更新方法，由行数判断改成根据时间判断
    04.17更新，同时统计所有的和>20db的
    :param sht:
    :return:
    """

    def count_inner(hb):
        if 7 <= hour < 19:
            hb[0] += 1
        elif 19 <= hour < 22:
            hb[1] += 1
        elif 22 <= hour < 24 or 0 <= hour < 7:
            hb[2] += 1

    hb1 = [0, 0, 0]
    hb2 = [0, 0, 0]
    hb3 = [0, 0, 0]
    hb4 = [0, 0, 0]
    hour = None
    regx = re.compile(r' (\d{1,2}):..')
    for i in range(3, 2080):
        if sht.range('a{}'.format(i)).value == '监测开始时间':
            hour_rex = regx.search(str(sht.range('a{}'.format(i + 1)).value))
            hour = int(hour_rex.group(1))
            # print(hour)
        if sht.range('j{}'.format(i)).value in [None, '机型']:  # 值对应机型列,如果有事件，统计架次
            continue
        # ---------4.17更新，统计lamax>20的，即在[lamaxp_all_day]中的航班的架次
        bg = float(sht.range('m4').value)
        maxla = sht.range('h{}'.format(i)).value
        if maxla is None:  # none表示背景干扰，赋值100以满足maxla - bg > 20，仅表示参与统计，此函数不影响数值计算
            maxla = 100
        # td = sht.range('e{}'.format(i)).value
        pd = sht.range('m{}'.format(i)).value
        if maxla - bg > 10.01:  # and td > 1.5:
            if pd in ['17R', '35L']:
                count_inner(hb1)  # 统计>20db
            elif pd in ['17L', '35R']:
                count_inner(hb2)  # 统计>20db
            elif pd in ['16R', '34L']:
                count_inner(hb3)  # 统计>20db
            elif pd in ['16L', '34R']:
                count_inner(hb4)  # 统计>20db
        # ---------
    return hb1 + [None, None] + hb2 + [None, None] + hb3 + [None, None] + hb4 + [None, None]


with open(r"C:\Users\Administrator\Desktop\新建文件夹\1.csv", 'w', newline='') as f:
    csv_f = csv.writer(f)
    for name, sht0 in yieldsht(r"C:\Users\Administrator\Desktop\新建文件夹"):
        result = [name] + count_hb(sht0)
        print(result)
        csv_f.writerow(result)
