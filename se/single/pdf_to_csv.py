# -*- coding: utf-8 -*-
# date: 2022-10-31
import pdfplumber
import os
import csv
import re


def wrap_try_except(func):
    import traceback

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            traceback.print_exc()

    return inner


def shimadzu_gc(func):
    """
    装饰器函数，为岛津gc模板做调整，在标记列为空的情况下，添加“-”。
    :param func:
    :return:
    """

    def inner(pdffile):
        s = func(pdffile)
        s = s.replace('         ', '     -    ')
        return s

    return inner


def agilent_gc(func):
    """
    装饰器函数，为安捷伦gc模板做调整，去除类型列类似“MM R”中间的空格
    :param func:
    :return:
    """

    def inner(pdffile):
        regx = re.compile(r'\d ([A-Z]{2} [A-Z])')
        s = func(pdffile)
        mmr = set(regx.findall(s))
        for i in mmr:
            s = s.replace(i, i.replace(' ', '_'))
        return s

    return inner


# @wrap_try_except
@shimadzu_gc
@agilent_gc
def readpdf(pdffile: str):
    """
    读取所有文本
    :param pdffile:绝对路径
    :return:
    """
    with pdfplumber.open(pdffile) as f:
        text = ''
        for page in f.pages:
            text += page.extract_text() + '\n'
            tables = page.extract_tables()  # 提取表格
    return text


def writecsv(text, csvfile):
    """
    写入到csv
    :param text: pdf读取的文本
    :param csvfile: 要保存到csv文件名
    :return:
    """
    with open(csvfile, 'w', newline='', encoding='gbk', errors='ignore') as f:
        writer = csv.writer(f)
        # 文本分行读取
        for line in text.splitlines():
            # 分隔每一行的元素，中间是2~3个空格
            writer.writerow(line.split())


def transe(pdffile, rename=False):
    if pdffile.lower().endswith('.pdf'):
        text = readpdf(pdffile)
        writecsv(text, outputpath := pdffile.replace(pdffile[-4:], '.csv'))
        # print(pdffile)
        if rename:
            os.rename(pdffile, pdffile + '.bak')
        return os.path.split(outputpath)[-1]


def run(rootpath, recursive=False, rename=False):
    """

    :param rename: 是否重命名pdf文件，为前端添加
    :param rootpath: oswalk根目录,或者单个文件
    :param recursive: 是否递归
    :return:
    """
    if os.path.isfile(rootpath):
        transe(rootpath, rename)
    elif os.path.isdir(rootpath):
        for root, _, files in os.walk(rootpath):
            for file in files:
                pdffile = os.path.join(root, file)
                transe(pdffile, rename)
            if not recursive:
                break


def extract_compunds(pdf_fp):
    """
    从安捷伦7890B的pdf报告提取结果
    :param pdf_fp:
    :return:
    """
    with pdfplumber.open(pdf_fp) as f:
        txt = ''.join([p.extract_text() for p in f.pages])
    regx_samplename = re.compile(r'数据文件.+\\(.*).D')
    samplename = regx_samplename.search(txt).group(1)
    regx_compunds = re.compile(r'-{18}\n(.+?)\n总量', re.DOTALL)
    compunds = regx_compunds.search(txt).group(1)
    if '-' * 18 in compunds:
        regx_compunds2 = re.compile('(.+)7890B.+-{18}\n(.+)', re.DOTALL)
        compunds = ''.join([(searchres := regx_compunds2.search(compunds)).group(1), searchres.group(2)])
    res = [(line.split()[-1], 0 if line.split()[-2] == '-' else float(line.split()[-2])) for line in
           compunds.split('\n')]
    return dict([(samplename, dict(res)), ])


if __name__ == '__main__':
    # path = os.path.split(os.path.realpath(__file__))[0]
    path = r"C:\Users\Administrator\Documents\xwechat_files\wxid_l30992hnzgxe21_5a2c\msg\file\2025-07\20250708102141(总氮).pdf"
    # run(path, recursive=False)
    print(readpdf(path))
    # print('完成')
