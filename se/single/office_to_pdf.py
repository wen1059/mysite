# -*- coding: utf-8 -*-
# date: 2022/7/21
import os
from win32com.client import constants, gencache
import sys
from glob import glob


def word2pdf(word):
    """
    word转pdf
    :param word:
    :return:
    """
    app = gencache.EnsureDispatch('Word.Application')
    file = app.Documents.Open(word, ReadOnly=1)
    file.ExportAsFixedFormat(OutputFileName=word.replace('.docx', '.pdf').replace('.doc', '.pdf'),
                             ExportFormat=constants.wdExportFormatPDF)
    file.Close()
    app.Quit()


def excel2pdf(xls):
    """
    excel转pdf
    :param xls:
    :return:
    """
    app = gencache.EnsureDispatch('Excel.Application')
    file = app.Workbooks.Open(xls, ReadOnly=1)
    file.ExportAsFixedFormat(Type=constants.xlTypePDF,  # excel和word参数名称和排序不一样，可录制宏查看
                             Filename=xls.replace('.xlsx', '.pdf').replace('.xls', '.pdf'))
    file.Close()
    app.Quit()


def findfiles(path):
    for root, _, files in os.walk(path):
        for file in files:
            yield os.path.join(root,file)


if __name__ == '__main__':
    # files = findfiles(r"C:\Users\Administrator\Desktop\学校相关\二年级\2A期末练习")
    files = sys.argv[1:]
    for file in files:
        if file.lower().endswith(('.docx', '.doc')):
            word2pdf(file)
        elif file.lower().endswith(('.xlsx', '.xls')):
            excel2pdf(file)
