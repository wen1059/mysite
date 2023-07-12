# -*- coding: utf-8 -*-
# date: 2023-3-25
import itertools


def gen_passwds(bignum, smallnum, dignum):
    """
    生成大写+小写+数字组合
    :param bignum: 大写字母个数上限
    :param smallnum: 小写字母个数上限
    :param dignum: 数字个数上限
    :return:
    """
    eng_big = [chr(i) for i in range(65, 91)]  # 大写字母列表
    eng_small = [chr(i) for i in range(97, 123)]  # 小写字母列表
    dig = [str(i) for i in range(10)]  # 数字列表
    num = [(a, b, c) for a in range(1, bignum + 1) for b in range(1, smallnum + 1) for c in
           range(1, dignum + 1)]  # 大写、小写、数字3种类型个数所有可能的组合

    for rpt_big, rpt_small, rpt_dig in num:
        for i in itertools.product(eng_big, repeat=rpt_big):
            for j in itertools.product(eng_small, repeat=rpt_small):
                for k in itertools.product(dig, repeat=rpt_dig):
                    yield ''.join(i + j + k)


for i in gen_passwds(1, 1, 1):
    print(i)
