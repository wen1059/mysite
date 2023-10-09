# -*- coding: utf-8 -*-
# date: 2023-10-9
"""
把航线转为拼音首字母，每个机场保留前两位，比如：阿布扎比-浦东-->ABPD
"""
import os
import subprocess
import sys
import xlwings
from xlwings.main import Book, Sheet
from pypinyin import lazy_pinyin


def trans_chs_to_pinyin(route: str):
    """
    把航线转为拼音首字母，每个机场保留前两位，比如：阿布扎比-浦东-->ABPD
    :param route:
    :return:
    """
    route_spl = route.split('-')
    # lazy_pinyin(airp[0:第一个汉字])[0：转换后是list，取0][0：拼音第一个字母]
    airp_py = ''.join([lazy_pinyin(airp[0])[0][0] + lazy_pinyin(airp[1])[0][0] for airp in route_spl])
    return airp_py.upper()


def trans_to_excel(xls):
    """
    转换excel里的航线
    :return:
    """
    app = xlwings.App(visible=False, add_book=False)
    file: Book = app.books.open(xls)
    sht: Sheet = file.sheets[0]
    routes = sht.range('f1').expand('down').value
    routes_py = [trans_chs_to_pinyin(route) for route in routes]
    sht.range('j1').options(transpose=True).value = routes_py
    file.save()
    file.close()
    app.quit()


if __name__ == '__main__':
    for file in sys.argv[1:]:
        trans_to_excel(file)
