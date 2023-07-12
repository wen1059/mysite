"""
selenium根据csv中的企业名称爬取
2021.11.04更新：水和空气整合在这个程序一起
"""
import os
from typing import List, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree
import traceback
import csv
import requests
import re
import time
import random
from itertools import zip_longest


def getid(qiye_name):
    """
    selenium取得企业id
    :return: source
    """

    def click_botton(xpath):
        botton = driver.find_element(by=By.XPATH, value=xpath)
        botton.click()

    #
    # def closetab():
    #     """
    #     关闭除第一个以外的标签页
    #     :return:
    #     """
    #     driver.close()
    #     driver.switch_to.window(driver.window_handles[1])
    #     driver.close()
    #     driver.switch_to.window(driver.window_handles[0])

    # click_botton('//*[@id="province"]/option[10]')  # 省选择上海
    # click_botton('//*[@id="city"]/option[2]')  # 地市选市辖区
    registerentername = driver.find_element(by=By.XPATH, value='//*[@id="registerentername"]')  # 输入企业名称框'
    registerentername.clear()
    registerentername.send_keys(qiye_name)
    click_botton('//*[@id="mainForm"]/div/input[6]')  # 搜索按钮
    # click_botton('/html/body/div[4]/div[3]/div/table/tbody/tr[2]/td[8]/a/img')  # 查看按钮
    # driver.switch_to.window(driver.window_handles[1])  # 切换到第二个标签
    # click_botton('/html/body/div[3]/div[1]/table[2]/tbody/tr[1]/td[2]/a/img')  # 水污染物按钮
    # driver.switch_to.window(driver.window_handles[2])  # 切换到第3个标签
    regx = re.compile('&dataid=(.*)')
    htm = driver.page_source
    tree = etree.HTML(htm)
    # print(htm)
    qiyeid = tree.xpath('/html/body/div[3]/div[3]/div/table/tbody/tr[2]/td[8]/a/@href')
    # print(qiyeid)
    hangye = tree.xpath('/html/body/div[3]/div[3]/div/table/tbody/tr[2]/td[5]/text()')
    try:
        qiyeid_ = regx.search(qiyeid[0]).group(1)
        return qiyeid_, hangye[0]
    except:
        print(rf'未找到企业 "{qiye_name}"')
        return 0, 0
    # closetab()


def getsource_home(id):
    """
    点开的第二个页面
    :param id:
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    htm = requests.get(
        'http://permit.mee.gov.cn/perxxgkinfo/xkgkAction!xkgk.action?xkgk=getxxgkContent&dataid={}'.format(
            id), headers=headers)
    return htm.text


def result_home(name, id, hy):
    tree = etree.HTML(getsource_home(id))
    airmeth = tree.xpath('//*[@id="apply_table"]/tr[4]/td/text()')[0]
    watermath = tree.xpath('//*[@id="apply_table"]/tr[7]/td/text()')[0]
    return name, hy, airmeth, watermath


def savehome(name, id, hy, f):
    res_air = csv.writer(f)
    try:
        res_air.writerow(result_home(name, id, hy))
        time.sleep(random.random() * 50)
    except Exception as e:
        print('savehome', e)


def getsource_air(id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    htm = requests.get(
        'http://permit.mee.gov.cn/perxxgkinfo/xkgkAction!xkgk.action?xkgk=approveAtmosphere_xkzgk&dataid={}&isVersion=&operate=readonly'.format(
            id), headers=headers)
    return htm.text


def dw_result_air(qiye_name, id):
    tree = etree.HTML(getsource_air(id))
    tables = {'grouptable': '主要排放口', 'apply_table1': '一般排放口'}
    result_air = []
    for table in tables:
        paifang_org = tree.xpath(f'//*[@id="{table}"]/tr/td/text()')  # 原始dw00x的列表
        paifang = [i.replace('\n', '').replace('\t', '').replace('\r', '') for i in paifang_org if
                   i.replace('\n', '').replace('\t', '').replace('\r', '') != '']  # 去除\n\t\r
        # print(paifang)
        indexda = [i for i in range(len(paifang)) if 'DA' in paifang[i]]  # 找到包含”DA“字符的索引
        paifang_final = [[qiye_name, tables[table]] + paifang[a:b] for a, b in
                         zip_longest(indexda, indexda[1:])]  # 以”DA“为开头分成多行
        result_air.extend(paifang_final)
        # print(result_air)
    return result_air


def saveair(name, id, f):
    res_air = csv.writer(f)
    try:
        pf_air = dw_result_air(name, id)
        res_air.writerows(pf_air)
        time.sleep(random.random() * 50)
    except Exception as e:
        print('saveair', e)


def getsource_water(id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    htm = requests.get(
        'http://permit.mee.gov.cn/perxxgkinfo/xkgkAction!xkgk.action?xkgk=approveWater_xkzgk&dataid={}&isVersion=&operate=readonly'.format(
            id), headers=headers)
    return htm.text


def dw_result_water(qiye_name, id):
    tree = etree.HTML(getsource_water(id))
    tables = {'fswrwinfo1': '主要排放口', 'fswrwinfo5': '一般排放口'}
    result_water = []
    for table in tables:
        paifang_org = tree.xpath(f'//*[@id="{table}"]/tr/td/text()')  # 原始dw00x的列表
        # print(paifang_org)
        paifang = [i.replace('\n', '').replace('\t', '').replace('\r', '') for i in paifang_org if
                   i.replace('\n', '').replace('\t', '').replace('\r', '') != '']  # 去除\n\t
        paifang_final = [[qiye_name, tables[table]] + paifang[9 * i:9 * (i + 1)] for i in
                         range(int(len(paifang) / 9))]  # 列表转为二维列表
        # print(paifang_final)
        result_water.extend(paifang_final)
    return result_water


def savewater(name, id, f):
    res_water = csv.writer(f)
    try:
        pf_water = dw_result_water(name, id)
        res_water.writerows(pf_water)
        time.sleep(random.random() * 50)
    except Exception as e:
        print('savewater', e)


def readnames():
    with open(r"C:\Users\Administrator\Desktop\新建文件夹\name.csv", newline='') as n:
        names = n.read().splitlines()
        for name in names:
            # print(name)
            id, hy = getid(name)
            if id:  # 若企业名称不对，getid会返回(0,0),加判断跳过，防止报错程序停止。
                yield name, id, hy


driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('http://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action')
path = r"C:\Users\Administrator\Desktop\新建文件夹"
os.chdir(path)
with open(r"result_home.csv", 'a', newline='') as f_home, \
        open(r"result_air.csv", 'a', newline='') as f_air, \
        open(r"result_water.csv", 'a', newline='') as f_water:
    for name, id, hy in readnames():
        savehome(name, id, hy, f_home)
        saveair(name, id, f_air)
        savewater(name, id, f_water)
        print(f'{name},done')
driver.close()

from ..single.合并excel import merge

files = ["result_home.csv", "result_air.csv", "result_water.csv"]
merge(path, *files)
