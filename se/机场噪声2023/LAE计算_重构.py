# -*- coding: utf-8 -*-
# date: 2023-12-8
import math
import os
import re
import time as time_
from datetime import datetime, time
from decimal import Decimal

import pandas as pd
import pymysql


class Mysqldb:
    """使用此类需要预先在mysql建立好库和表"""

    def __init__(self):
        self.con = pymysql.connect(host='localhost',
                                   port=3306,
                                   user='root',
                                   passwd='WenLiang10072518',
                                   database='airport_noise'
                                   )
        self.curse = self.con.cursor()

    def ins_to_tab(self, tab, values):
        """
        写入表，insert语句根据表名和values中元素做调整
        用replace into 可实现有就更新，没有就添加功能，但需要表设置（点位&日期）索引
        :param tab:要写入的表
        :param values: 需要写入的值，列表形式
        :return:
        """
        sql = f'''INSERT INTO {tab} 
            ( pri, 点位, 日期,  Ldn, Nd_有效, Nn_有效, Nd_总, Nn_总, 记录时间 ) 
            VALUES 
            (NULL, \'{values[0]}\', \'{values[1]}\', \'{values[2]}\', '{values[3]}\', \'{values[4]}\', \'{values[5]}\', \'{values[6]}\', now())'''
        self.curse.execute(sql)
        self.con.commit()


def findfile24(walkpath: str):
    for root, _, files in os.walk(walkpath):
        for file in files:
            if file.lower().endswith(('.xlsx', '.xls')) and not file.startswith('~$'):
                yield os.path.join(root, file)


def get_pos_and_date(filename):
    """
    获取点位和日期
    :param filename:xlsx名称
    :return:
    """
    if f24n_re := re.search(r'(\d{1,2}.*#)(\d{2,4}.*).xls*', filename):
        position_, date_ = f24n_re.group(1), f24n_re.group(2)
    else:
        position_, date_ = '00', '0000',
    return position_, date_


def readfile24(xls: str) -> (pd.DataFrame,):
    """
    读取24小时文件
    :param xls: 绝对路径
    :return: (df1_day, df1_night, df2_day, df2_night)
    """

    def splt_day_and_night(df):
        """
        把df按昼夜分成两部分
        :param df: 读取出的原始df
        :return:
        """
        df.loc[:, 'startTime'] = df['startTime'].apply(lambda x: datetime.time(x))  # datetime转成time用于判断昼夜。
        df_day = df[(time(6, 0, 0) <= df['startTime']) & (df['startTime'] < time(22, 0, 0))]
        df_night = pd.concat([df, df_day]).drop_duplicates(keep=False)
        return df_day, df_night

    df_org = pd.read_excel(xls, header=5)
    df_org = df_org[df_org['LAE(10)'] != 'LAE(10)']  # 去除每个小时表格的表头。
    df1 = df_org.dropna(subset='LAE(10)')  # 仅保留LAE(10)有值的行，df1用于数据计算。
    df2 = df_org.dropna(subset='机型').ffill()  # 仅保留有航班的行，df2用于统计原始架次，对计算无影响。.ffill()向上填充空值.
    return splt_day_and_night(df1) + splt_day_and_night(df2)


def cal_ldn(df_day: pd.DataFrame, df_night: pd.DataFrame) -> float:
    """
    计算Ldn，公式（2）
    :param df_day:
    :param df_night:
    :return:
    """
    df_night['LAE(10)'] = df_night['LAE(10)'] + 10  # 夜间lae修正
    df_all = pd.concat([df_day, df_night])  # 合并day和night
    laes: pd.Series = df_all.loc[:, 'LAE(10)']  # lae列
    result = 10 * math.log10(1 / 86400 * laes.apply(lambda x: math.pow(10, 0.1 * x)).sum())
    return float(Decimal(f'{result}').quantize(Decimal('0.0')))


if __name__ == '__main__':
    import 机场噪声_2021虹桥.day_epn_acu_虹桥 as oldcal

    db = Mysqldb()
    path_xlss = r'\\10.1.78.254\环装-实验室\实验室共享\2023鸡场\__投递到这里自动计算__'
    while True:
        for file24 in findfile24(path_xlss):
            print(filename := os.path.split(file24)[1])
            pos, dat = get_pos_and_date(filename)
            df_cal_day, df_cal_night, df_allflt_day, df_allflt_night = readfile24(file24)
            rst_ldn = cal_ldn(df_cal_day, df_cal_night)
            nd_effective, nn_effective = df_cal_day.shape[0], df_cal_night.shape[0]
            nd_all, nn_all = df_allflt_day.shape[0], df_allflt_night.shape[0]
            insdata = [pos, dat, rst_ldn, nd_effective, nn_effective, nd_all, nn_all]
            db.ins_to_tab('新标准计算', insdata)
        oldcal.run_oneday_week(path_xlss, 'day_精密_2023', 'week虹桥')
        time_.sleep(3)
    # db.con.close()
