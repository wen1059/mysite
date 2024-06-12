# -*- coding: utf-8 -*-
# date: 2023-3-13
"""
py7zr, tarfile, zipfile
"""
import os
import py7zr
import shutil

root = r"C:\Users\Administrator\Desktop"
os.chdir(root)
targetfolder = '新建文件夹'

archive: py7zr.SevenZipFile  # 无用，为了代码提示
with py7zr.SevenZipFile(f'{targetfolder}.7z', 'w') as archive:
    archive.writeall(targetfolder)

with py7zr.SevenZipFile('archive.7z', 'r') as archive:
    archive.extractall()

# base_name：压缩后的zip文件的路径，只写文件名会保存到当前目录下，要保存到上层目录可以“../name”
# root_dir:压缩目标，会压缩这个目录下的所有文件和文件夹
# base_dir是下层目录/文件，存在时只压缩base_dir这个文件夹/文件， 否则压缩root_dir下所有的文件夹和文件，一般不使用。
shutil.make_archive(base_name='archive', format='zip', root_dir=root, base_dir=targetfolder)
