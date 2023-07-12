# -*- coding: utf-8 -*-
# date: 2022/6/22
"""
分割excel的sheet到单个文件
"""
import sys
import xlwings
from xlwings.main import Book, Sheet
from tqdm import tqdm


def wrap_try_except(func):
    import traceback

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            traceback.print_exc()

    return inner


@wrap_try_except
def split(book_: str):
    app = xlwings.App(visible=False, add_book=False)
    file_org: Book = app.books.open(book_)
    sht: Sheet
    for sht in tqdm(file_org.sheets, desc='正在分割', colour='green'):
        sht.visible = True
        f_new: Book = app.books.add()
        sht0 = f_new.sheets[0]
        sht.copy(before=sht0)
        sht0.delete()
        f_new.save(book_.replace('.xlsx', f'_{sht.name}.xlsx'))
        f_new.close()
    app.quit()


if len(sys.argv) > 1:
    book = sys.argv[1]
else:
    book = input('拖放excel于此黑框')

split(book.replace('\"', ''))
