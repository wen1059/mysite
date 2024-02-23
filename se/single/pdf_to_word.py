# -*- coding: utf-8 -*-
# date: 2022/7/21
import os
from pdf2docx import Converter


def convert(pdf: str, rename=False):
    """
    pdf转word
    :return:
    """
    conv = Converter(pdf)
    conv.convert(pdf.replace('.pdf', '.docx'), start=0, end=None)
    conv.close()
    if rename:
        os.rename(pdf, pdf + '.bak')


def findpdfs(path):
    os.chdir(path)
    for root, _, files in os.walk(path):
        for file in files:
            if file.lower().endswith('.pdf'):
                yield os.path.abspath(file)


if __name__ == '__main__':
    # for file in findpdfs(r'C:\Users\Administrator\Desktop\新建文件夹 (3)'):
    #     convert(file)
    convert(r"C:\Users\Administrator\Documents\WeChat Files\wxid_l30992hnzgxe21\FileStorage\File\2024-02\Shimudzu MRM 筛查结果.pdf")
