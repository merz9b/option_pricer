# -*- coding: utf-8 -*-
# @Time    : 2018/10/19 15:44
# @Author  : Xin Zhang
# @File    : test_scrap_2.py

import requests
import pandas as pd
from lxml import etree
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import datetime
import time

# option = webdriver.ChromeOptions()
# option.add_argument('headless')
# brs = webdriver.Chrome(options= option)

brs = webdriver.Chrome()
brs.get('http://www.nanhuacapital.com/fd/')
brs.implicitly_wait(2)

#
try:
    enter_1 = brs.find_element_by_xpath(
        '//*[@id="layui-m-layer1"]/div[2]/div/div')
    brs.refresh()
except NoSuchElementException:
    pass

s = brs.find_element_by_xpath(
    '//*[@id="app"]/div/div[1]/div[3]/button/div/div[2]/div[1]/div/input')
s.click()

# calendar
btn = brs.find_element_by_xpath('//*[@id="demo2"]')
btn.click()

btn_2 = brs.find_element_by_xpath(
    '//*[@id="layui-laydate1"]/div/div[2]/table/tbody/tr[4]/td[3]')
btn_2.click()
time.sleep(2)

table = brs.find_element_by_xpath('//*[@id="tablevalue"]')

table_html = table.get_attribute('outerHTML')

pd.read_html(table_html)


print(table.text)

dir(table)


brs.close()


rsp = requests.post(
    'http://www.luzhengqh.com/rest/weixin/getOptionPrice',
    data={'contractcode': 'A1901', 'expiryDate': '2018-11-19'})

print(rsp.json())
