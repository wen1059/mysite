# -*- coding: utf-8 -*-
# date: 2022/2/16

"""
将多个excel中所有的sheet合并到一个新的excel
"""

# 方法1
# import xlwings as xw
# wb = xw.Book('example1.xlsx')
# sht = wb.sheets['sheet1']
# new_wb = xw.Book()
# new_sht = new_wb.sheets[0]
# sht.api.Copy(Before = new_sht.api)
# ***现在可直接sht.copy(before=new_sht)***

# 方法2
# 经过漫长的斗争，终于找到了答案。来自xlwings源代码：https://github.com/xlwings/xlwings/pull/1216/files
# source_sheet.range.copy(destination_sheet.range)
# 换句话说：
# wb.sheets['Sheet1'].range('A1:A6').copy(wb.sheets['Sheet2'].range('A1:A6'))
# 它也适用于从一个工作簿到另一个工作簿。

import os
from glob import iglob
from tqdm import tqdm
import xlwings
from xlwings.main import Book, Sheet


def merge(path, *partfiles):
    """
    :param path: # excel所在文件夹的绝对路径
    :param partfiles: # 只合并部分文件,文件名
    :return:
    """
    app = xlwings.App(visible=False, add_book=False)
    f_merge: Book = app.books.add()
    sht0: Sheet = f_merge.sheets[0]
    os.chdir(path)
    if os.path.exists('合并.xlsx'):
        os.remove('合并.xlsx')
    # 如果指定文件，那么只合并这些文件，否则合并当前文件夹内所有文件
    if partfiles:
        files = [os.path.join(path, partfile) for partfile in partfiles]
    else:
        files = iglob(path + r'\\**\\*.xls*', recursive=True)
    for file in tqdm(files, desc='正在合并', colour='green'):
        if file.startswith('~') or (not file.endswith(('.xlsx', '.xls', '.csv'))):
            continue
        xlsx: Book = app.books.open(file)
        for sht in xlsx.sheets:
            # sht.api.Copy(Before=sht0.api)
            sht.copy(before=sht0)
        xlsx.close()
    sht0.delete()
    f_merge.save('合并.xlsx')
    f_merge.close()
    app.quit()


if __name__ == '__main__':
    path = os.path.split(os.path.realpath(__file__))[0]
    merge(path)
