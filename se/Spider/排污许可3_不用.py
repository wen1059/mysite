"""
根据企业名称和id，爬取废水数值
不用，已整合到另一文件
"""
import requests
from selenium import webdriver
from lxml import etree
import re
import csv
import time
import os
import random
import traceback


def getsource(id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    htm = requests.get(
        'http://permit.mee.gov.cn/perxxgkinfo/xkgkAction!xkgk.action?xkgk=approveWater_xkzgk&dataid={}&isVersion=&operate=readonly'.format(
            id), headers=headers)
    return htm.text


def readname():
    with open(r"C:\Users\Administrator\Desktop\新建文件夹\name.csv", newline='') as f:
        lines = csv.reader(f)
        for line in lines:
            yield line


def dw_result(qiye_name, id):
    tree = etree.HTML(getsource(id))
    paifang_org = tree.xpath('//*[@id="fswrwinfo1" or @id="fswrwinfo5"]/tr/td/text()')  # 原始dw00x的列表
    # print(paifang_org)
    paifang = [i.replace('\n', '').replace('\t', '').replace('\r', '') for i in paifang_org if
               i.replace('\n', '').replace('\t', '').replace('\r', '') != '']  # 去除\n\t
    paifang_final = [[qiye_name] + paifang[9 * i:9 * (i + 1)] for i in range(int(len(paifang) / 9))]  # 列表转为二维列表
    print(paifang_final)
    return paifang_final


def savewater():
    with open(r"C:\Users\Administrator\Desktop\新建文件夹\result.csv", 'w', newline='') as f:
        csv_res = csv.writer(f)
        for name, id in readname():
            try:
                csv_res.writerows(dw_result(name, id))
            except Exception as e:
                print(traceback.print_exc())
            time.sleep(random.random() * 50)


savewater()
