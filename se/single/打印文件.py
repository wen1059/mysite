"""
打印成pdf，需要设置pdf打印机为默认，设置好输出文件夹，取消pdf预览
"""
import os
import time
import win32print
# import tempfile
import win32api


def print_file(filename):
    # open(filename,"r")
    win32api.ShellExecute(
        0,
        "print",
        filename,
        '/d:"%s"' % win32print.GetDefaultPrinter(),
        ".",
        0
    )


path = r"C:\Users\Administrator\Desktop\新建文件夹 (2)\新建文件夹"
os.chdir(path)
for file in os.listdir():
    print_file(file)
    time.sleep(3)
