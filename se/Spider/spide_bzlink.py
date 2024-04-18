# -*- coding: utf-8 -*-
# date: 2024-4-11
"""
爬取生态环境部网站标准链接
"""
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree


def search_bzlink():
    """
    爬取标准名称和pdf链接
    :return:
    """

    driver = webdriver.Edge()
    driver.implicitly_wait(10)
    driver.get(r'https://www.mee.gov.cn/searchnew/?searchword=1')
    searchword = driver.find_element(by=By.XPATH, value=r'//*[@id="keyword"]')  # 搜索框
    for num in range(1, 1335):
        searchword.clear()
        searchword.send_keys(f'HJ {num}')
        driver.find_element(by=By.XPATH, value='//*[@id="quickSearch"]').click()  # 检索按钮
        htm = driver.page_source
        tree = etree.HTML(htm)
        link = tree.xpath('//*[@id="list2"]/li[1]/a/@herf')
        yield link
    driver.close()


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'}
for i in search_bzlink():
    print(i)
