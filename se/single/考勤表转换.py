# -*- coding: utf-8 -*-
# date: 2023-11-15
"""
把钉钉考勤表转换为自己的模板
"""
import os
import sys
from pypinyin import lazy_pinyin

import pandas as pd


def read_dd(file: str | os.PathLike) -> pd.DataFrame:
    """
    读取钉钉考勤表
    :param file: 钉钉的excel,绝对路径
    :return:
    """
    df = pd.read_excel(file, header=2, usecols='a,i:k')  # 读取excel，保留aijk列
    df = df[df['打卡结果'].isin(['正常', '外勤'])]  # 筛选保留打卡结果['正常', '外勤']行
    df['打卡时间'] = pd.to_datetime(df['打卡时间'])  # 时间列转为datetime格式
    df['打卡日期'] = df['打卡时间'].dt.strftime('%Y-%m-%d')  # 打卡时间拆分为y-m-d和time
    df['打卡时间'] = df['打卡时间'].dt.strftime('%H:%M')
    # 如果是外勤，时间后面加上地址
    # df.apply中lamdba后面的x是Series，axis=1表示x是每一行的Series，这个Series的Index是column名。
    # Series.apply中lamdba后面的x是单个元素，没有axis参数。
    df['打卡时间'] = df[['打卡时间', '打卡结果', '打卡地址']].apply(
        lambda x: ''.join(x[['打卡时间', '打卡地址']]) if x['打卡结果'] == '外勤' else x['打卡时间'], axis=1)
    df = df[['打卡日期', '姓名', '打卡时间']]  # 保留这三列
    # df转为新的数据结构{date:{name:time, ...}, ...}
    dict_temp = {}
    for date_, name_, time_ in df.values:
        if date_ not in dict_temp:
            dict_temp.setdefault(date_, {})
        if name_ not in dict_temp[date_]:
            dict_temp[date_].setdefault(name_, time_)
        else:
            dict_temp[date_].setdefault(name_ + '2', time_)
    # 转为适合模板的df。过程为：转为df，按index(人名，key=拼音)排序，转置，按index(日期)排序。
    # pandas的sort中lamdba规则和buildin函数不一样。pandas中x为pd.Index/pd.Series，返回值也是此数据结构；buildin排序中x为单个元素。
    df_out = pd.DataFrame(dict_temp).sort_index(
        key=lambda x: pd.Index([''.join(lazy_pinyin(i)) for i in x])).T.sort_index()
    # print(df_out.columns)
    return df_out


def write_dd(df: pd.DataFrame, file: str | os.PathLike) -> None:
    """
    将转换好的df写入到excel
    :param df:
    :param file:
    :return:
    """
    with pd.ExcelWriter(file, mode='a') as ew:
        df.to_excel(ew, sheet_name='convert')


if __name__ == '__main__':
    # file = sys.argv[1]
    file = r"C:\Users\Administrator\Desktop\考勤匹配\副本上海市环境监测技术装备有限公司_原始记录表_20230905-20230918.xlsx"
    df = read_dd(file)
    write_dd(df, file)
    print('完成')
    os.system('pause')
