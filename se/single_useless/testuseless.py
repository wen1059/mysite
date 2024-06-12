# -*- coding: utf-8 -*-
# date: 2024-5-23
from copy import deepcopy
import xlwings as xw
import pandas as pd


def sudukohelp():
    solutions = []

    def readboard():
        f = xw.books.active
        data = f.sheets[0].range('a1:i9').value
        df = pd.DataFrame(data)
        df = df.astype('int').fillna(0)
        return df.values.tolist()

    board = readboard()
    for b in board:
        print(b)
sudukohelp()