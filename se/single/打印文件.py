"""
打印成pdf，需要设置pdf打印机为默认，设置好输出文件夹，取消pdf预览
"""
import os
import time
import win32print
# import tempfile
import win32api
import sys
from glob import glob
import os


def print_file(filepath, printer_name=None):
    # open(filename,"r")
    win32api.ShellExecute(
        0,
        "print",
        filepath,
        f'/d:"{printer_name}"' if printer_name else None,
        ".",
        0
    )


if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = glob(os.path.join(os.path.split(sys.argv[0])[0], '*.*'))
for file in files:
    print_file(file)
    time.sleep(3)
