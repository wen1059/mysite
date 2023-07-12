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
            # tables = page.extract_tables() # 提取表格
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


def runsingle(pdffile, rename=False):
    if pdffile.lower().endswith('.pdf'):
        text = readpdf(pdffile)
        writecsv(text, pdffile.replace(pdffile[-4:], '.csv'))
        print(pdffile)
        if rename:
            os.rename(pdffile, pdffile + '.bak')


def run(rootpath, recursive=False, rename=False):
    """

    :param rename: 是否重命名pdf文件，为前端添加
    :param rootpath: oswalk根目录,或者单个文件
    :param recursive: 是否递归
    :return:
    """
    if os.path.isfile(rootpath):
        runsingle(rootpath, rename)
    elif os.path.isdir(rootpath):
        for root, _, files in os.walk(rootpath):
            for file in files:
                pdffile = os.path.join(root, file)
                runsingle(pdffile, rename)
            if not recursive:
                break


if __name__ == '__main__':
    # path = os.path.split(os.path.realpath(__file__))[0]
    path = r"Z:\实验室共享\04 有机室\B44489-44508506-PAMS.pdf"
    run(path, recursive=False)
    print('完成')
