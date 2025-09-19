import xlwings

from xlwings import Book, Sheet


def foo():
    # 数值汇总，方便niantie到表格
    summary = []
    book = xlwings.books.active
    for sheet in book.sheets:
        summary.append(sheet.range('f16:f18').value)
    book.sheets.add(before=book.sheets[0])
    book.sheets[0].range('a1').options(transpose=True).value = summary


def foo2():
    # 数值填入表单
    summary = []
    book = xlwings.books.active
    for sheet in book.sheets:
        for num in range(16, 19):
            line = [sheet.range(f'a{num}').value, sheet.name, sheet.range(f'f{num}').value]
            summary.append(line)
    book.sheets.add(before=book.sheets[0])
    book.sheets[0].range('a1').value = summary


foo2()
