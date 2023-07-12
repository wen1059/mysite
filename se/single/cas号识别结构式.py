'''
chemicalbook，由cas号爬取结构式
'''
import requests
import csv
import os


# from PIL import Image
# from io import BytesIO

def savepic(cas, savepath):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    htm = requests.get('https://www.chemicalbook.com/CAS/GIF/{}.gif'.format(cas), headers=headers)
    with open(os.path.join(savepath, '{}.gif'.format(cas)), 'wb') as f:
        f.write(htm.content)


def readcas(csvpath):
    with open(csvpath, newline='') as f:
        lines = csv.reader(f)
        for line in lines:
            yield line[0]


for cas in readcas(r"C:\Users\Administrator\Desktop\新建文件夹 (2)\新建文本文档.txt"):
    savepic(cas,r"C:\Users\Administrator\Desktop\新建文件夹 (2)")