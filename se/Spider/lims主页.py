# -*- coding: utf-8 -*-
# date: 2022/2/22
from selenium import webdriver
from selenium.webdriver.common.by import By

option = webdriver.EdgeOptions()
option.add_experimental_option("detach", True)
driver = webdriver.Edge(options=option)
driver.get('http://10.1.31.200:8000/indexv3.aspx')
username = driver.find_element(by=By.XPATH, value='//*[@id="username"]')
username.send_keys('wenl@shzb')
passwd = driver.find_element(by=By.XPATH, value='//*[@id="password"]')
passwd.send_keys('wenl@shzb1')
login = driver.find_element(by=By.XPATH, value='/html/body/div/div[1]/div/form/div/input[3]')
login.click()
