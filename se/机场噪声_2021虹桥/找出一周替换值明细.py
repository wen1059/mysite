import os
import xlwings

app_r = xlwings.App(add_book=False)
app_w = xlwings.App(add_book=False)
app_he = xlwings.App(add_book=False)
f_read = app_r.books.open(r"C:\Users\Administrator\Desktop\文件夹-r-w\新建文件夹 (3)\新建文本文档.xlsx")
sht_read = f_read.sheets[0]
f_write = app_w.books.open(r"C:\Users\Administrator\Desktop\文件夹-r-w\新建文件夹 (3)\带明细1.xlsx")
sht_write = f_write.sheets[0]
f_he = app_he.books.add()
rowflag = 1
flag_eli = False
fhelst = []
for i in range(1, 1800):
    jx, hl, qj, sz = sht_read.range(f'a{i}').value, sht_read.range(f'b{i}').value, sht_read.range(
        f'c{i}').value, sht_read.range(f'd{i}').value
    if not jx:
        continue
    # print(jx, hl, qj, sz)
    rowflag += 1
    if '.xlsx' in jx:
        rowflag += 1
        fhelst = []
        f_he.close()
        f_he = app_he.books.open(os.path.join(r"C:\Users\Administrator\Desktop\文件夹-r-w\新建文件夹 (3)\合并不要管这个文件夹", jx))
        sht_he = f_he.sheets[0]
        for j in range(1, 14560):
            fhelst.append([f'{j}行'] + sht_he.range(f'a{j}:p{j}').value)
    sht_write.range(f'a{rowflag}').value = [jx, hl, qj, sz]
    rowflag += 1
    for k in fhelst:
        xh, st, et, ml, lepn, te, l10, l15, mla, hbh, jx_he, qj_he, fxfx, pd, hl_he, bz, eli = k
        if st == '监测开始时间':
            if fhelst[fhelst.index(k) + 1][-1] == 1:
                flag_eli = True
                # print(True)
            else:
                flag_eli = False
        # print(jx_he, hl_he, qj_he)
        if (jx_he, hl_he, qj_he) == (jx, hl, qj):
            # print('find')
            if flag_eli:
                sht_write.range(f'a{rowflag}').value = k[:-1] + ['1']
            else:
                sht_write.range(f'a{rowflag}').value = k[:-1]
            rowflag += 1

f_write.save()
app_r.quit()
app_w.quit()
app_he.quit()
