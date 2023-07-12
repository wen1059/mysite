import os
from glob import glob

for file in glob(r'C:\数据\**\*.cdf', recursive=True):
    print('删除文件{}'.format(file))
    os.remove(file)
print('已完成')
input()
