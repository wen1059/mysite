# -*- coding: utf-8 -*-
# date: 2023-6-2
"""
填充excel单元格，空单元格取上一格内容
"""
import xlwings
from xlwings.main import Sheet, Book


def fill(cols):
    """

    :param cols: 要填充的列,a列和b列就写'ab'
    :param rows: 要填充的总行数
    :return:
    """
    file = xlwings.books.active
    sht0: Sheet = file.sheets[0]
    rows = sht0.used_range.last_cell.row
    for col in cols:
        flag = None
        values = sht0.range(f'{col}1:{col}{rows}').value
        for i in range(len(values)):
            if values[i]:
                flag = values[i]
            else:
                values[i] = flag
        sht0.range(f'{col}1').options(transpose=True).value = values


fill('ab')
