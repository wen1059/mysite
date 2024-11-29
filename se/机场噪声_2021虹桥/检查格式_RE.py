# -*- coding: utf-8 -*-
# date: 2024-10-30
import pandas as pd
import numpy as np
import sys
import os


def check(file):
    """
    检查lepn0，备注
    :param file:
    :return:
    """
    df = pd.read_excel(file, header=None, usecols='d,j,o', names=['lepn', '机型', '备注'])  # 保留三列
    df.index = df.index + 1  # 索引+1保持与excel一致
    df = df[~df['机型'].isin(('机型', np.nan))]  # 去除空行和表头
    df = df[['lepn', '备注']]  # 去除机型列
    df = df[(df['lepn'] == 0) | (df['lepn'].isnull() & df['备注'].isnull()) | (
            ~df['备注'].isnull() & ~df['lepn'].isnull())]  # lepn=0 or 两个都空（缺备注） or 两个都不空（多备注）
    df['file'] = os.path.split(file)[-1]  # 添加文件名字段
    df = df[['file', 'lepn', '备注']]  # 调整顺序
    return df


def findfiles(walkpath: str):
    # if len(sys.argv) > 1:
    #     for file in sys.argv[1:]:
    #         yield file
    # else:
    for root, _, files in os.walk(walkpath):
        for file in files:
            if file.lower().endswith(('.xlsx', '.xls')) and not file.startswith('~$'):
                yield os.path.join(root, file)


def showcheckresult(walkpath):
    df_all = pd.DataFrame(columns=['file', 'lepn', '备注'])
    for file in findfiles(walkpath):
        df = check(file)
        if not df.empty:
            df_all = pd.concat([df_all, df])
    return df_all.to_html()
