import math
import os
import re
import pymysql
import xlwings
import time
import shutil
import traceback
from decimal import Decimal


def yieldsht(walkpath, app_24):
    """
    生成每个要处理的表
    :return:
    """
    # app_24 = xlwings.App(visible=False, add_book=False)  # 待计算文件
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
    # app_24.kill()


app24 = xlwings.App(add_book=False)
for fname, sht in yieldsht(r"\\bg\环境报告审核人共享\最终版5.25原版", app24):
    count = 0
    bggr = sht.range('o1:o1700').options(transpose=True).value
    for i in bggr:
        if i == '背景干扰':
            count += 1
    print(fname, count)
