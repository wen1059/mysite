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
    conv.convert(outputname := pdf.replace('.pdf', '.docx'), start=0, end=None)
    conv.close()
    if rename:
        os.rename(pdf, pdf + '.bak')
    return outputname


def findpdfs(path):
    os.chdir(path)
    for root, _, files in os.walk(path):
        for file in files:
            if file.lower().endswith('.pdf'):
                yield os.path.abspath(file)


if __name__ == '__main__':
    # for file in findpdfs(r'C:\Users\Administrator\Desktop\新建文件夹 (3)'):
    #     convert(file)
    convert(r"C:\Users\Administrator\Documents\xwechat_files\wxid_l30992hnzgxe21_5a2c\msg\file\2025-03\EP11.0 Nitrogen 1247E(1).pdf")
