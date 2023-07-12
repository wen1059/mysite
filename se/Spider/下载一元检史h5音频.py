# -*- coding: utf-8 -*-
# date: 2022-11-21
import requests
import os
from pypinyin import lazy_pinyin
import csv


def name2py(name: str):
    """
    汉字转拼音首字母
    :param name: 汉字
    :return: 首字母（包含数字）
    """
    result = ''
    for i in lazy_pinyin(name):
        result += i[0]
    return result


def download(name, pyname):
    """
    下载m4a音频
    :param name: 需要保存为的文件名
    :param pyname: 拼音首字母，用于下载。
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    m4file = requests.get(
        f'https://jxgc-file.oss-accelerate.aliyuncs.com/yyjs/20200102/{pyname}.m4a', headers=headers)

    with open(f'{name}.m4a', 'wb') as f:
        f.write(m4file.content)


os.chdir(r"C:\Users\Administrator\Downloads\乱世三百年-闲话南北朝之天下归一")
with open('name.csv') as f:
    lines = csv.reader(f)
    for fullname, name in lines:
        pyname = name2py(name)
        download(fullname, pyname)
        print(fullname)
