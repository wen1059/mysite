# -*- coding: utf-8 -*-
# date: 2023-4-23
"""
移除excel的加密/保护/编辑限制
"""
import os
import sys
# import xlwings
import shutil
import re
from win32com.client import gencache, constants


def transxls_using_win32com(func):
    def inner(orgfile: str):
        if orgfile.endswith('.xls'):
            app = gencache.EnsureDispatch('Excel.Application')
            file = app.Workbooks.Open(orgfile)
            # FileFormat 可以在excel里录制宏查看
            file.SaveAs(newfile := orgfile.replace('.xls', '.xlsx'), FileFormat=constants.xlOpenXMLWorkbook)
            file.Close()
            app.Quit()
            os.remove(orgfile)
            return newfile
        return orgfile

    return inner


@transxls_using_win32com
def trans_xls_to_xlsx(orgfile: str):
    """
    xls转为xlsx,不用，已被装饰器改写
    :param orgfile: str|PathLike,绝对路径
    :return:
    """
    # if orgfile.endswith('.xls'):
    #     app = xlwings.App(visible=False, add_book=False)
    #     file = app.books.open(orgfile)
    #     file.save(newfile := orgfile.replace('.xls', '.xlsx'))
    #     app.quit()
    #     os.remove(orgfile)
    #     return newfile
    return orgfile


def unpack(archive):
    """
    将xlsx解压到同级目录同名文件夹下
    :param archive:压缩包绝对路径
    :return:
    """
    shutil.unpack_archive(archive, unpackdir := archive.replace('.xlsx', ''), 'zip')
    return unpackdir


def findxml(dir):
    """
    查找每个sheet的xml文件
    :return:
    """
    for root, _, files in os.walk(os.path.join(dir, 'xl/worksheets')):
        for file in files:
            if file.endswith('.xml'):
                yield os.path.join(root, file)


def removeprotect(xml):
    """
    移除加密
    :param xml:
    :return:
    """
    regx = re.compile('<sheetProtection.+?/>')
    with open(xml, encoding='utf-8') as f:
        text = f.read()
        newtext = regx.sub('', text)
    with open(xml, 'w', encoding='utf-8') as f:
        f.write(newtext)


def repack(file, unpackdir):
    """
    重新打包成xlsx
    :param file: 原xlsx路径
    :param unpackdir:之前解压到的文件夹路径
    :return:
    """
    shutil.make_archive(base_name=file, format='zip', root_dir=unpackdir)


def run(file):
    file = trans_xls_to_xlsx(file)
    unpackdir = unpack(file)
    os.remove(file)
    for xml in findxml(unpackdir):
        removeprotect(xml)
    repack(file, unpackdir)
    os.rename(f'{file}.zip', file)
    shutil.rmtree(unpackdir)
    outputfilename = os.path.split(file)[-1]
    return outputfilename


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        file = r"C:\Users\Administrator\Documents\xwechat_files\wxid_l30992hnzgxe21_5a2c\msg\file\2025-08\设备清单(更新至复证).xls"
    run(file)
