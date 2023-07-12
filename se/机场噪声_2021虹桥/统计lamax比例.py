"""
统计24小时excel中lamax的值50~60，60~70...的个数
"""

import os
import csv

import xlwings


def yieldsht(walkpath):
    """
    生成每个要处理的表
    :return:
    """
    app_24 = xlwings.App(visible=False, add_book=False)  # 待计算文件
    for root, _, files in os.walk(walkpath):
        for filexlsx in files:
            if ('.xls' not in filexlsx) or '~$' in filexlsx:
                continue
            file24path = os.path.join(root, filexlsx)
            file24 = app_24.books.open(file24path)  # 24小时文件
            yield file24.name, file24.sheets[0]
            file24.close()
    app_24.quit()


with open(r"C:\Users\Administrator\Desktop\新建文件夹 (2)\lamaxbl.csv", 'w', newline='') as f:
    csv_f = csv.writer(f)
    for fname, sht in yieldsht(r"\\bg\环境报告审核人共享\2021\虹桥机场\最终版5.25"):
        lamaxs_org = sht.range('h1:h1700').options(transpose=True).value  # h列的值
        lamaxs = [i for i in lamaxs_org if isinstance(i, float)]  # 保留数字
        # print(lamaxs)
        count = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # [50,60),[60,70),...[90,inf)的个数
        for i in lamaxs:
            if 50 <= i < 55:
                count[0] += 1
            elif 55 <= i < 60:
                count[1] += 1
            elif 60 <= i < 65:
                count[2] += 1
            elif 65 <= i < 70:
                count[3] += 1
            elif 70 <= i < 75:
                count[4] += 1
            elif 75 <= i < 80:
                count[5] += 1
            elif 80 <= i < 85:
                count[6] += 1
            elif 85 <= i < 90:
                count[7] += 1
            elif i >= 90:
                count[8] += 1
        print(fname, count)
        csv_f.writerow([fname] + count)
