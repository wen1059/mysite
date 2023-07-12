"""
根据CAS号查找化合物名称，chemicalbook查询。
"""
# import bs4
import re
import xlwings


def translate1(cas_num):
    """
    爱化学搜索，正则式解析。
    :param cas_num:
    :return:
    """
    htm = requests.get(r'http://www.ichemistry.cn/chemistry/{}.htm'.format(cas_num))
    htm.encoding = htm.apparent_encoding
    text = htm.text
    ser = re.compile(r'CAS:{}\|(.+)_爱化学</TITLE>'.format(cas_num))
    result = ser.search(text)
    if result:
        return result.group(1)
    return 'error'


def translate2(cas_num):
    """
    chemicalbook查询，正则式解析。
    :param cas_num:
    :return:
    """
    htm = requests.get(r'https://www.chemicalbook.com/Search.aspx?keyword={}'.format(cas_num))
    # htm.encoding=htm.apparent_encoding
    text = htm.text
    ser = re.compile(r';">(.+)</a></td>')
    result = ser.findall(text)
    if result:
        return result[1]
    return 'error'


def translate(cas_num):
    """
    chemicalbook查询，bs4解析。
    :param cas_num: 输入的cas号
    :return: 中文名
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    htm = requests.get(r'https://www.chemicalbook.com/Search.aspx?keyword={}'.format(cas_num), headers=headers)
    soup = bs4.BeautifulSoup(htm.text, features='lxml')
    elem = soup.select('td.rtd a')
    try:
        return elem[1].get_text()
    except:
        return 'error'


def translate3(cas_num):
    """
    chemicalbook查询，xpath解析。
    :param cas_num: 输入的cas号
    :return: 中文名
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    htm = requests.get(r'https://www.chemicalbook.com/Search.aspx?keyword={}'.format(cas_num), headers=headers)
    tree = etree.HTML(htm.text)
    a = tree.xpath('//*[@id="mbox"]/tr[3]/td[2]/a')
    print(a[0].text)


# xlsfile = xlwings.books.active
# sht = xlsfile.sheets.active
# for i in range(1, sht.range('b1').expand('down').rows.count):
#     cas_num = sht[i, 1].value
#     chsname = translate(cas_num)
#     sht[i, 10].value = chsname

import requests
from lxml import etree
import csv


def trans(cas):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    htm = requests.get(f'https://www.chemicalbook.com/Search.aspx?keyword={cas}', headers=headers, timeout=5)
    tree = etree.HTML(htm.text)
    name = tree.xpath('//*[@id="mbox"]/tr[3]/td[2]/a/text()')
    if name:
        return name[0]


def readcas(csvpath):
    with open(csvpath, newline='') as f:
        lines = csv.reader(f)
        for line in lines:
            if line:
                yield line[0]


for cas in readcas(r"C:\Users\Administrator\Desktop\新建文件夹\castoname.csv"):
    name = trans(cas)
    print(cas, name)
