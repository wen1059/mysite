import os
import xlwings


def yieldsht(walkpath, app_24):
    """
    生成每个要处理的表
    :return:
    """
    for root, _, files in os.walk(walkpath):
        for filexlsx in files:
            if filexlsx[-5:-1] != '.xls' or '~$' in filexlsx:
                continue
            file24path = os.path.join(root, filexlsx)
            file24 = app_24.books.open(file24path)  # 24小时文件
            # shtcount = file24.sheets.count  # sheet数量
            # for sc in range(shtcount):
            #     sht = file24.sheets[sc]  # sht：其中一天的sheet
            yield file24.name, file24.sheets[0]
            file24.close()


app_hb = xlwings.App(add_book=False)
for innerwalkpath, _, _ in os.walk(os.getcwd()):
    if innerwalkpath == os.getcwd():
        continue
    file_hb = app_hb.books.add()
    sht_hb = file_hb.sheets[0]
    i = 1
    fname = ''
    for fname, sht24 in yieldsht(innerwalkpath, app_hb):
        sht_hb.range(f'a{i}').value = sht24.range('a1:p2080').value
        i += 2080
    file_hb.save(os.path.join(innerwalkpath, fname + '合并.xlsx'))
    file_hb.close()
app_hb.quit()
