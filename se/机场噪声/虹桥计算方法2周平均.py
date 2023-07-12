import xlwings
import re
import math
import os


def cal():
    jc_all = 0
    sig_l = []
    for mmd,jx, jc, lepnk in list_row:
        sig = math.pow(10, 0.1 * lepnk) * jc
        sig_l.append(sig)
        jc_all += jc
    return jc_all, round(10 * math.log10(math.fsum(sig_l) / jc_all), 1)


sht = xlwings.books.active.sheets.active
list_row = []
for row in range(2, 280):
    jx = sht.range('c{}'.format(row)).value
    mdd = sht.range('d{}'.format(row)).value
    # if mdd is None:
    #     continue
    jc = sht.range('f{}'.format(row)).value
    lepnk = sht.range('e{}'.format(row)).value
    if len(list_row) != 0 and (mdd != list_row[0][0] or jx != list_row[0][1]):
        jc_all, zpj = cal()
        sht.range('g{}'.format(row - 1)).value = [jc_all, zpj]
        list_row.clear()
    list_row.append((mdd, jx, jc, lepnk))
