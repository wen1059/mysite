# -*- coding: utf-8 -*-
# date: 2023-10-27
"""
把3个voc称样量sheet的内容都放到sheet1，为了谱图读取
"""
import xlwings
from xlwings.main import Book, Sheet


file: Book = xlwings.books.active
s: Sheet
val = []
for i in range(file.sheets.count):
    sht:Sheet = file.sheets[i]
    lc = sht.used_range.last_cell
    row = lc.row
    v = sht.range(f'a1:d{row}').value
    val.extend(v)
file.sheets.add(before=file.sheets[0])
file.sheets[0].range('a1').value = val
