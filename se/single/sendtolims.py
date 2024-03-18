# -*- coding: utf-8 -*-
# date: 2024-2-22
"""
把文件复制一份到谱图读取的目录
"""

import shutil
import os
import sys

try:
    import pyperclip
except ImportError:
    os.system('pip install pyperclip')
    import pyperclip

basedir = r'\\10.1.210.119\ETims\建科'
instrumentname = os.path.split(os.path.realpath(__file__))[1].replace('.py', '')
# instrumentname = 'SEMTEC_212'
batch = pyperclip.paste()
files = sys.argv[1:]
# 删除旧批文件夹
for oldbatch in os.listdir(os.path.join(basedir, instrumentname)):
    shutil.rmtree(os.path.join(basedir, instrumentname, oldbatch))
# 建立新批文件夹
os.mkdir(dst := os.path.join(basedir, instrumentname, batch))
for file in files:
    shutil.copy(file, dst)
