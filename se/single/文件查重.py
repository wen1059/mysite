# -*- coding: utf-8 -*-
# date: 2022/5/26
import hashlib
import os
import sys
import stat
import csv
import time
from tqdm import tqdm


def get_file_md5(file_name):
    """
    计算文件的md5
    :param file_name:
    :return:
    """
    m = hashlib.md5()  # 创建md5对象
    with open(file_name, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            m.update(data)  # 更新md5对象
    return m.hexdigest()  # 返回md5对象


def check_duplicate(walkpath):
    """
    根据MD5检查重复文件
    :param walkpath: 根目录
    :return: 重复文件的路径列表[(路径1，路径2),...]
    """
    file_md5_dic = {}
    file_duplicate = []
    for root, dirs, files in os.walk(walkpath):
        # if dirs[-2:] in ['.D', '.M']:
        #     continue
        for file in files:
            file = os.path.join(root, file)
            md5 = get_file_md5(file)
            if md5 in file_md5_dic:
                file_duplicate.append((file_md5_dic[md5], file))
                continue
            file_md5_dic.setdefault(md5, file)
    return file_duplicate


def printresult(walkpath, file_duplicate):
    """
    显示结果
    :param walkpath:
    :param file_duplicate:
    :return:
    """
    if not file_duplicate:
        print('未发现重复项')
        sys.exit(0)
    with open(os.path.join(walkpath, '文件查重结果.csv'), 'w', newline='', encoding='utf-8') as f:
        csv_f = csv.writer(f)
        csv_f.writerow((time.ctime(),))
        for d in file_duplicate:
            csv_f.writerow(d)
            print(d)


def del_duplicate(file_duplicate):
    """
    删除重复项
    :param file_duplicate: check_duplicate()返回值。
    :return:
    """
    req = input('是否删除重复项（Y/N）：')
    if req.upper() == 'Y':
        for a, b in file_duplicate:
            try:
                os.remove(b)
            except:
                os.chmod(b, stat.S_IWRITE)
                os.remove(b)


if __name__ == '__main__':
    # walkpath = os.getcwd()
    walkpath = r"C:\Users\Administrator\Documents\WeChat Files"
    file_duplicate = check_duplicate(walkpath)
    printresult(walkpath, file_duplicate)
    del_duplicate(file_duplicate)
