# -*- coding: utf-8 -*-
# date: 2023-6-16
import os.path

import pikepdf
import sys


def unlock(fp: str):
    """
    移除pdf编辑限制的密码
    :param fp: 需要解密的pdf，绝对路径
    :return:
    """
    assert fp.lower().endswith('.pdf')
    with pikepdf.open(fp, allow_overwriting_input=True) as pdf:
        pdf.save()
        return os.path.split(fp)[-1]


if __name__ == '__main__':
    for file in sys.argv[1:]:
        unlock(file)
