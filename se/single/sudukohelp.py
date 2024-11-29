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
        df = df.fillna(0).astype('int')
        return df.values.tolist()

    board = readboard()

    # board = [[0, 0, 0, 6, 0, 2, 0, 0, 0],
    #          [9, 0, 2, 0, 0, 5, 0, 0, 0],
    #          [0, 0, 3, 7, 0, 0, 0, 0, 0],
    #          [0, 0, 8, 2, 6, 0, 3, 0, 1],
    #          [0, 0, 0, 0, 9, 0, 0, 8, 0],
    #          [1, 0, 0, 0, 0, 0, 0, 0, 0],
    #          [0, 7, 0, 0, 5, 0, 1, 0, 0],
    #          [0, 8, 0, 0, 2, 0, 0, 9, 0],
    #          [5, 0, 0, 1, 4, 0, 0, 3, 0]]

    def conflict(digit, index):  # 检查冲突
        row = index // 9  # 线性index转换成二维行列
        col = index % 9

        def sqare3x3():  # 返回小的九宫格
            row_top = row // 3 * 3  # 小九宫格左上角的坐标
            col_top = col // 3 * 3
            return [board[i][j] for i in range(row_top, row_top + 3) for j in range(col_top, col_top + 3)]

        if digit in board[row] or digit in [x[col] for x in board] or digit in sqare3x3():
            return True
        return False

    posss = []  # 空格的位置索引，0~80
    for pos in range(81):
        if board[pos // 9][pos % 9] == 0:
            posss.append(pos)

    def backtrack(t=0):
        if t == len(posss):
            solutions.append(deepcopy(board))
            return
        pos = posss[t]
        for digit in range(1, 10):
            if not conflict(digit, pos):
                board[pos // 9][pos % 9] = digit
                backtrack(t + 1)
                board[pos // 9][pos % 9] = 0  # 回溯到上一步时，需要将这次的值设回0

    backtrack()

    return solutions


for res in sudukohelp():
    for line in res:
        print(line)
