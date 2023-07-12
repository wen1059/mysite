"""
selenium抓取企业id
"""
import requests
from selenium import webdriver
from lxml import etree
import re
import csv
import time
import os
import random


def click_botton(xpath):
    botton = driver.find_element_by_xpath(xpath)
    botton.click()


def initpage():
    """
    初始化网页
    :return:
    """
    click_botton('//*[@id="province"]/option[10]')  # 省选择上海
    click_botton('//*[@id="city"]/option[2]')  # 地市选市辖区
    click_botton('//*[@id="mainForm"]/div/input[6]')  # 查询按钮


def getonepagename():
    """
    爬取一个页面
    :return: [(企业名称，id),...]
    """
    regx = re.compile('&dataid=(.*)')
    htm = driver.page_source
    tree = etree.HTML(htm)
    qiyenames = tree.xpath('/html/body/div/div[3]/div/table/tbody/tr/td[4]/@title')
    qiyeids = tree.xpath('/html/body/div/div[3]/div/table/tbody/tr/td[8]/a/@href')
    qiyeids_ = [regx.search(i).group(1) for i in qiyeids]
    result = [i for i in zip(qiyenames, qiyeids_)]
    return result


def nextpage():
    """
    转到下一页
    :return:
    """
    click_botton("/html/body/div[4]/div[4]/div/a[text()='下一页']")
    time.sleep(random.random() * 50)


def saveid():
    initpage()
    with open(r"C:\Users\Administrator\Desktop\新建文件夹\name.csv", 'w', newline='') as f:
        csv_f = csv.writer(f)
        while True:
            # for i in range(3):
            onepage = getonepagename()
            csv_f.writerows(onepage)
            try:
                nextpage()
            except Exception as e:
                print(e)
                break


driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('http://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action')
saveid()
driver.close()
