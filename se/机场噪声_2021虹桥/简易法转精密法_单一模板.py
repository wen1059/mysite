import re
import os
from mypkg.walk import Walk
import xlwings


def trans(sht_old, sht_new):
    start_new = [7 + 70 * i for i in range(24)]
    start_old = [7 + 76 * i for i in range(24)]
    allvalue = []  # 24组数据
    for s in start_old:
        temp = []  # 每个小时的数据
        for i in range(s, s + 35):
            if sht_old.range(f'f{i}').value is None:
                break
            temp.append(sht_old.range(f'a{i}:b{i}').value +
                        sht_old.range(f'l{i}:q{i}').value +
                        sht_old.range(f'f{i}:k{i}').value)
        allvalue.append(temp)
    for i in range(24):
        sht_new.range(f'a{start_new[i]}').value = allvalue[i]

    sht_new.range('c4').value = sht_old.range('c4').value
    sht_new.range('i4').value = sht_old.range('g4').value



w = Walk(filetype='xls', path=r"C:\Users\Administrator\Desktop\虹桥噪声桌面\浦东优先分析点位\old")
for filename_old in w.filepaths:
    app = xlwings.App(visible=True, add_book=False)
    file_old = app.books.open(filename_old)
    sht_old = file_old.sheets[0]
    file_new = app.books.open(r"C:\Users\Administrator\Desktop\虹桥噪声桌面\浦东优先分析点位\new\浦东精密法分析记录.xlsx")
    sht_new = file_new.sheets[0]
    trans(sht_old, sht_new)
    file_old.close()
    file_new.save(os.path.join(r"C:\Users\Administrator\Desktop\虹桥噪声桌面\浦东优先分析点位\new", os.path.basename(filename_old)))
    file_new.close()
    # break
    app.quit()
