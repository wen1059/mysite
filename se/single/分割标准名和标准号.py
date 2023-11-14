# -*- coding: utf-8 -*-
# date: 2023-3-8
import re
import csv
import xlwings
from xlwings.main import Book, Sheet


def splitname(std: str):
    regx = re.compile(
        'GB.+|HJ.+|US.+|LY.+|DB.+|JC.+|JG.+|ISO.+|CJ.+|WS.+|SL.+|NY.+|QX.+|QB.+|DG.+|DZ.+|T/SSESB.+|T/SHAEPI.+|YY.+')
    part2 = regx.search(std)
    if part2:
        part2 = part2.group()
    else:
        part2 = ''
    part1 = std.replace(part2, '')
    return part1, part2


file = xlwings.books.active
sht: Sheet = file.sheets[0]
methodnane = sht.range('c1:c5084').value
splmnane = [splitname(i)[1] for i in methodnane]
sht.range('d1').options(transpose=True).value = splmnane

# with open(r"C:\Users\Administrator\Desktop\新建 文本文档.CSV", 'w', newline='') as f:
#     writer = csv.writer(f)
#     for line in standards.splitlines():
#         res = splitname(line)
#         writer.writerow(res)
