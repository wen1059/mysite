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

# base_name是文件保存到哪个目录，
# root_dir是压缩包根目录，
# base_dir是下层目录，存在时只压缩base_dir这个文件夹， 否则压缩root_dir下所有的文件夹和文件
shutil.make_archive(base_name='archive', format='zip', root_dir=root, base_dir=targetfolder)
