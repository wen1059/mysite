# -*- coding: utf-8 -*-
# date: 2023-6-16
import pikepdf
import sys


def unlock(filein: str):
    """
    移除pdf编辑限制的密码
    :param filein: 需要解密的pdf，绝对路径
    :param fileout: 解密后保存名称
    :return:
    """
    if filein.lower().endswith('.pdf'):
        with pikepdf.open(filein) as pdf_:
            pdf_.save(filein.replace(filein[-4:], '_PasswordRemoved.pdf'))


def unlock_cover(filein: str):
    """
    解密后覆盖原文档
    :param filein:
    :return:
    """
    if filein.lower().endswith('.pdf'):
        with pikepdf.open(filein, allow_overwriting_input=True) as pdf_:
            pdf_.save()


if __name__ == '__main__':
    for file in sys.argv[1:]:
        unlock_cover(file)
