# -*- coding: utf-8 -*-
# date: 2023-6-16
import os.path

import pikepdf
import sys


def unlock(fp: str, cover=True):
    """
    移除pdf编辑限制的密码
    :param cover: 是否覆盖
    :param fp: 需要解密的pdf，绝对路径
    :param fileout: 解密后保存名称
    :return:
    """
    if fp.lower().endswith('.pdf'):
        with pikepdf.open(fp, allow_overwriting_input=True) as pdf:
            if cover:
                pdf.save()
                return os.path.split(fp)[-1]
            pdf.save(outputpath := fp.replace(fp[-4:], '_PasswordRemoved.pdf'))
            return os.path.split(outputpath)[-1]


if __name__ == '__main__':
    for file in sys.argv[1:]:
        unlock(file)
