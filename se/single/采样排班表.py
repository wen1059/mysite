# -*- coding: utf-8 -*-
# date: 2022-11-28
import re
import os
import time
import xlwings
from xlwings.main import Book, Sheet


def readstripe():
    """
    读取已排班的人员和设备
    :return:
    """
    dict_stripe = {}  # {日期：[{去除的人名集合},{去除的仪器集合}]}
    sht0: Sheet = file.sheets['采样任务安排']
    tab = sht0.range('a2').expand().value  # 除第一行外的全部数据
    for line in tab:
        if line[0] not in dict_stripe:
            dict_stripe.setdefault(line[0], [set(), set()])
        #  line[5]的值,加号替换为短号、去除（车）、按顿号分割、存入人名set
        if line[5]:
            dict_stripe[line[0]][0].update([i for i in line[5].replace('+', '、').replace('（车）', '').split('、')])
        #  line[9]的值，re查找所有三位数字（设备编号），存入set
        if line[9]:
            dict_stripe[line[0]][1].update(re.findall('\d{3}', line[9]))
    return dict_stripe


def writename():
    """
    写入空余人员名单
    :return:
    """
    result = []
    sht1: Sheet = file.sheets['人员']
    names = sht1.range('a2').expand('down').value  # A列的人名模板
    dict_stripe = readstripe()
    for date in dict_stripe:
        names_copy = [i if i not in dict_stripe[date][0] else None for i in names.copy()]
        result.append([date] + names_copy)
    sht1.range('b1').options(transpose=True).value = result


def writeinstrument():
    result = []
    sht2: Sheet = file.sheets['设备']
    instruments = sht2.range('a2').expand('down').value  # A列的设备模板
    dict_stripe = readstripe()
    for date in dict_stripe:
        # instruments中的三位数字如果在dict_stripe[date][1]中，用None替代
        names_copy = [i if re.findall('\d{3}', i)[0] not in dict_stripe[date][1] else None for i in instruments.copy()]
        result.append([date] + names_copy)
    sht2.range('b1').options(transpose=True).value = result


if __name__ == '__main__':
    file = xlwings.books.active
    writename()
    writeinstrument()
