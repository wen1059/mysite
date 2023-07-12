import os
import xlwings

app_r = xlwings.App(add_book=False)
app_he = xlwings.App(add_book=False)
f_read = app_r.books.open(r"C:\Users\Administrator\Desktop\文件夹-r-w\新建文件夹 (3)\新建文本文档.xlsx")
sht_read = f_read.sheets[0]
f_he = app_he.books.add()
sht_he = f_he.sheets[0]
flag_eli = False
row_r_flag = 0
for row_r in range(1, 1800):
    jx = sht_read.range(f'a{row_r}').value
    if not jx:
        continue
    if '.xlsx' not in jx:
        continue
    row_r_flag = row_r + 1
    f_he.close()
    f_he = app_he.books.open(os.path.join(r"C:\Users\Administrator\Desktop\文件夹-r-w\新建文件夹 (3)\合并不要管这个文件夹", jx))
    sht_he = f_he.sheets[0]
    for j in range(1, 14560):
        if sht_he.range(f'a{j}').value == '监测开始时间':
            if sht_he.range(f'p{j + 1}').value == 1:
                flag_eli = True
            else:
                flag_eli = False
        jx_he, hl_he, qj_he = sht_he.range(f'j{j}').value, sht_he.range(f'n{j}').value, sht_he.range(f'k{j}').value
        if jx_he in [None, '机型']:
            continue
        if flag_eli:
            sht_read.range(f'e{row_r_flag}').value = [jx_he, hl_he, qj_he]
            row_r_flag += 1
app_he.quit()
