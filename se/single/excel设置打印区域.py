# -*- coding: utf-8 -*-
# date: 2025-3-6
import sys

import xlwings as xw
from xlwings.main import Book, Sheet


def set_print_area(fp):
    app = xw.App(visible=False, add_book=False)
    book: Book = app.books.open(fp)
    sheet: Sheet
    for sheet in book.sheets:
        sheet.page_setup.print_area = 'a1:r39'
    book.save()
    app.quit()


if __name__ == '__main__':
    for fp in sys.argv[1:]:
        set_print_area(fp)
