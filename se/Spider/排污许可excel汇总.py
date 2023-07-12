"""
由测试报告汇总到汇总表
新增测试报告汇总到一起
"""
import os
import csv
from glob import glob

# from typing import List, Any, Union

try:
    import xlwings
except:
    os.system('pip install xlwings')
    import xlwings
from xlwings.main import *


def namedic(path):
    """
    文件名取前11位单号
    :param path:xls文件夹
    :return:字典：{前11位：全名}
    """
    result = {}
    for root, _, files in os.walk(path):
        for file in files:
            if '排污许可限值及标准汇总' in file:
                result.setdefault('排污许可限值及标准汇总', file)
                continue
            if '.xls' in file.lower():
                result.setdefault(file[0:11], file)
    return result


def xmdic(sht):
    """
    读取she文件，生成{项目：值}
    :param sht:
    :return:
    """
    dic = {}
    flag = 100
    for i in range(1, 100):
        xm = sht.range(f'b{i}').value
        if xm == 'Analyte Chinese Name':
            flag = i
        zhi = sht.range(f'g{i}').value
        if i > flag:
            if not xm:
                continue
            dic.setdefault(xm, zhi)
    return dic


def huizong(path):
    """
    汇总到表
    :return:
    """
    name = namedic(path)  # xls名称的字典
    app = xlwings.App(visible=True, add_book=False)
    huizong = app.books.open(os.path.join(path, name['排污许可限值及标准汇总']))  # 汇总Excel文件
    shthz = huizong.sheets[1]  # 汇总sht
    she_dic = {}
    for i in range(2, 5000):
        danhao = shthz.range(f'e{i}').value  # 单号
        if not danhao:
            continue
        if danhao != shthz.range(f'e{i - 1}').value:  # ！=表示新一单
            try:
                fileshe = app.books.open(os.path.join(path, name[danhao]))
                shtshe = fileshe.sheets[0]
                she_dic = xmdic(shtshe)
                # print(she_dic)
                fileshe.close()
            except Exception as e:
                print(e)
                continue
        try:  # 两边项目名称不一样读取不到
            shthz.range(f'r{i}').value = she_dic[shthz.range(f'i{i}').value]
        except Exception as e:
            print(f'第{i}行未识别', e)
    input()
    # huizong.save()
    # huizong.close()
    # app.quit()


def hebin(path):
    """
    合并测试报告
    :param path:路径
    :return:
    """
    app = xlwings.App(visible=True, add_book=False)
    with open(os.path.join(path, 'hebin.csv'), 'w', newline='') as f:
        csv_f = csv.writer(f)
        t = namedic(path).copy()
        if tt := '排污许可限值及标准汇总' in t:
            t.pop(tt)
        for file in t.values():
            xlsfile = app.books.open(os.path.join(path, file))
            sht = xlsfile.sheets[0]
            value = [(xlsfile.name,) + i for i in xmdic(sht).items()]
            csv_f.writerows(value)
            xlsfile.close()
    app.quit()


def hebin2(path):
    """
    直接合并多个excel到一个sheet，不做任何修改
    :param path:
    :return:
    """
    files = glob(path + '\\*.xls')
    app = xlwings.App(visible=True, add_book=False)
    with open(os.path.join(path, 'hebin2.csv'), 'w', newline='', errors='ignore') as f:
        writer = csv.writer(f)
        for file in files:
            fx: Book = app.books.open(file)
            sht: Sheet = fx.sheets[0]
            l: list[list[str | None]] = sht.range('a1:az200').value
            # 删除除最后一行外的空行
            for i in reversed(l[:-1]):
                if i[0] is None:
                    l.remove(i)
            # 第一列添加xls文件名，但不用每一行都添加
            l[0].insert(0, os.path.basename(file))
            for i in l[1:-1]:
                i.insert(0, None)
            writer.writerows(l)
            fx.close()
    app.quit()


if __name__ == '__main__':
    path = r"C:\Users\Administrator\Desktop\新建文件夹 (2)"
    hebin2(path)
    # hebin(path)
    # huizong(path)
