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


app = xlwings.App(visible=True, add_book=False)
w = Walk(filetype='xls', path=r"C:\Users\Administrator\Desktop\虹桥噪声桌面\浦东优先分析点位\new")
for filename_new in w.filepaths:
    file_new = app.books.open(filename_new)
    sht_new = file_new.sheets[0]
    filename_old = re.search(r'\d{2}#\d{4}', filename_new).group() + '.xlsx'
    file_old = app.books.open(os.path.join(r"C:\Users\Administrator\Desktop\虹桥噪声桌面\浦东优先分析点位\old", filename_old))
    sht_old = file_old.sheets[0]
    # print(filename_new, filename_old)
    trans(sht_old, sht_new)
    file_new.save()
    file_new.close()
    file_old.close()
app.quit()
