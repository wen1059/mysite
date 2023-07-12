# -*- coding: utf-8 -*-
# date: 2022/2/22
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('http://10.1.1.80:81/lims/')
username=driver.find_element(by=By.XPATH,value='//*[@id="username"]')
username.send_keys('wenliang')
passwd = driver.find_element(by=By.XPATH,value='//*[@id="password"]')
passwd.send_keys('wenl')
login = driver.find_element(by=By.XPATH,value='//*[@id="btn_login"]')
login.click()
fxlr = driver.find_element(by=By.XPATH,value='//*[@id="B8DAB1349C77487F927FE2CFB5AC55BF"]')
fxlr.click()
