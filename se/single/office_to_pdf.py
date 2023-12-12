# -*- coding: utf-8 -*-
# date: 2022/7/21
import os
from win32com.client import constants, gencache


def words2pdf(words: list[str], rename=False):
    """
    word转pdf
    :param rename:
    :param words: 文件绝对路径的列表
    :return:
    """
    app = gencache.EnsureDispatch('Word.Application')
    for word in words:
        file = app.Documents.Open(word, ReadOnly=1)
        file.ExportAsFixedFormat(OutputFileName=word.replace('.docx', '.pdf').replace('.doc', '.pdf'),
                                 ExportFormat=constants.wdExportFormatPDF)
        file.Close()
        if rename:
            os.rename(word, word + '.bak')
    app.Quit()


def excels2pdf(xlss: list[str], rename=False):
    """
    excel转pdf
    :param xlss:
    :return:
    """
    app = gencache.EnsureDispatch('Excel.Application')
    for xls in xlss:
        file = app.Workbooks.Open(xls, ReadOnly=1)
        file.ExportAsFixedFormat(Type=constants.xlTypePDF,  # excel和word参数名称和排序不一样，可录制宏查看
                                 Filename=xls.replace('.xlsx', '.pdf').replace('.xls', '.pdf'))
        file.Close()
        if rename:
            os.rename(xls, xls + '.bak')
    app.Quit()


def findfiles(path):
    os.chdir(path)
    officefile = {'words': [], 'excels': []}
    for root, _, files in os.walk(path):
        for file in files:
            if file.lower().endswith(('.docx', '.doc')):
                officefile['words'].append(os.path.abspath(file))
            elif file.lower().endswith(('.xlsx', '.xls')):
                officefile['excels'].append(os.path.abspath(file))
    return officefile


if __name__ == '__main__':
    ofs = findfiles(r"C:\Users\Administrator\Desktop\学校相关\二年级\2A期末练习")
    words2pdf(ofs['words'])
    excels2pdf(ofs['excels'])
