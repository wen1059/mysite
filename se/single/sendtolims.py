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

rootdir = r'\\10.1.210.119\ETims\建科'
instrumentname = os.path.split(os.path.realpath(__file__))[1].replace('.py', '')
batch = pyperclip.paste()
files = sys.argv[1:]
for oldbatch in os.listdir(os.path.join(rootdir, instrumentname)):
    shutil.rmtree(os.path.join(rootdir, instrumentname, oldbatch))
os.mkdir(dst := os.path.join(rootdir, instrumentname, batch))
for file in files:
    shutil.copy(file, dst)
