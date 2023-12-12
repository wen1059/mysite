# -*- coding: utf-8 -*-
# date: 2023-10-9
"""
把航线转为拼音首字母，每个机场保留前两位，比如：阿布扎比-浦东-->ABPD
"""
import datetime
import sys

import pandas as pd
import xlwings
from pypinyin import lazy_pinyin


def trans_chs_to_pinyin(route: str):
    """
    把航线转为拼音首字母，每个机场保留前两位，比如：阿布扎比-浦东-->ABPD
    :param route:
    :return:
    """
    route_spl = route.split('-')
    # lazy_pinyin(airp[0:第一个汉字])[0：转换后是list，取0][0：拼音第一个字母]
    airp_py = ''.join([lazy_pinyin(airp[0])[0][0] + lazy_pinyin(airp[1])[0][0] for airp in route_spl])
    return airp_py.upper()


def trans_to_excel(xls):
    """
    转换excel里的航线
    :return:
    """
    # app = xlwings.App(visible=False, add_book=False)
    # file: Book = app.books.open(xls)
    file = xlwings.books.active
    for sht in file.sheets:
        routes = sht.range('f1').expand('down').value
        routes_py = [trans_chs_to_pinyin(route) for route in routes]
        sht.range('j1').options(transpose=True).value = routes_py
    # file.save()
    # file.close()
    # app.quit()


def read_route(xls: str):
    """

    :param xls:
    :return:
    """
    df = pd.read_excel(xls, sheet_name=-1)
    df = df.dropna(subset=['航线'], how='any')
    df['起飞/降落时间'] = df['起飞/降落时间'].apply(
        lambda x: datetime.datetime.combine(datetime.date.fromisoformat('2023-12-09'), x))
    df['航线'] = df['航线'].apply(trans_chs_to_pinyin)
    df['起飞/降落'] = df['航线'].apply(lambda x: '起飞' if x[0:2] == 'HQ' else '降落')
    df = df[['序号', '起飞/降落时间', '航班号', '机型', '起飞/降落', '起飞/降落方向', '使用跑道', '航线',
             '航班性质 客机/货机']]
    return df


if __name__ == '__main__':
    # file = sys.argv[1]
    file = r"C:\Users\Administrator\Desktop\新建文件夹 (2)\航班时刻表 (12.1-12.9)(3).xls"
    transed_data = read_route(file)
    # print(transed_data)
    transed_data.to_excel(file.replace('.xls', '.xlsx'), index=False)
