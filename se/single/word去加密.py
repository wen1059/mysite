# -*- coding: utf-8 -*-
# date: 2023-4-23
"""
移除word的加密/保护/编辑限制
"""
import os
import sys
import shutil
import re
from win32com.client import gencache, constants


def trans_doc_to_docx(orgfile: str):
    """
    xls转为xlsx
    :param orgfile: str|PathLike,绝对路径
    :return:
    """
    if orgfile.endswith('.doc'):
        app = gencache.EnsureDispatch('Word.Application')
        file = app.Documents.Open(orgfile)
        file.SaveAs(newfile := orgfile.replace('.doc', '.docx'), FileFormat=constants.wdFormatXMLDocument)
        file.Close()
        app.Quit()
        os.remove(orgfile)
        return newfile
    return orgfile


def unpack(archive):
    """
    将xlsx解压到同级目录同名文件夹下
    :param archive:压缩包绝对路径
    :return:文件所在目录下的同名文件夹
    """
    shutil.unpack_archive(archive, unpackdir := archive.replace('.docx', ''), 'zip')
    return unpackdir


def findxml(dir):
    """
    查找每个sheet的xml文件
    :param dir: unpack目录
    :return:
    """
    return os.path.join(dir, 'word/settings.xml')


def removeprotect(xml):
    """
    移除加密
    :param xml:
    :return:
    """
    regx = re.compile('<w:documentProtection.+?/>')
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
    :return:/**/*.xlsx.zip
    """
    shutil.make_archive(base_name=file, format='zip', root_dir=unpackdir)


def run(file):
    file = trans_doc_to_docx(file)
    unpackdir = unpack(file)
    os.remove(file)
    xml = findxml(unpackdir)
    removeprotect(xml)
    repack(file, unpackdir)
    os.rename(f'{file}.zip', file)
    shutil.rmtree(unpackdir)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        file = r"C:\Users\Administrator\Desktop\新建文件夹\新建文件夹 (3)\非甲气袋验收sop.doc"
    run(file)
