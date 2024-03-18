# -*- coding: utf-8 -*-
# date: 2024-3-5
"""
excel vba会调用这个文件
"""
# hello.py

import xlwings as xw


def helloworld():
    wb = xw.books.active
    wb.sheets[0]['A1'].value = 'Hello World!'


helloworld()
