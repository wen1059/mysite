# -*- coding: utf-8 -*-
# date: 2023-7-6
"""
查找lims数据库
"""
from typing import Tuple, Any

import pymysql
import xlwings
from xlwings.main import Book, Sheet


class Limsdb:

    def __init__(self):
        """
        连接数据库
        """
        self.connt = pymysql.connect(host='10.1.1.82',
                                     port=3306,
                                     user='cs',
                                     passwd='123456',
                                     database='dbs_lims2_release'
                                     )
        self.curse = self.connt.cursor()

    def close(self):
        """
        关闭数据库
        :return:
        """
        self.curse.close()
        self.connt.close()

    def searchrasprojectno(self, ordershowno):
        """
        根据样品名查项目编号
        :param ordershowno:样品编号
        :return:
        """
        sql = f'SELECT lo.rasprojectno FROM lims_orders lo WHERE lo.ordershowno="{ordershowno}"'
        self.curse.execute(sql)
        self.connt.commit()
        rst = self.curse.fetchone()[0]
        return rst

    def search_by_projectno(self, testno, projectno):
        """
        谱图读取通用模板用，根据项目编号和测试名称查询出样品编号、分析项、分析项谱图名、结果
        :param testno: 基础测试库中的”测试名称“
        :param projectno:项目名称
        :return:
        """
        sql = f"""
            SELECT
                lo.ordershowno,
                lr.analyte,
                la.eqanalyte,
                lr.final_result 
            FROM
                lims_results lr
                LEFT JOIN lims_orders lo ON lr.ordno = lo.ordno
                LEFT JOIN lims_analytes la ON ( lr.testcode = la.testcode AND lr.method = la.method AND lr.analyte = la.analyte ) 
            WHERE
                lr.testno = "{testno}" 
                AND lr.rasprojectno = "{projectno}" 
            ORDER BY
                lo.ordno,
                la.sorter
                """
        self.curse.execute(sql)
        self.connt.commit()
        rst = self.curse.fetchall()
        return rst

    def search_by_runno(self, runno):
        """
        根据批号查询出样品编号、分析项、分析项谱图名、结果
        :param runno:
        :return:
        """
        sql = f"""
            SELECT
                lo.ordershowno,
                lr.analyte,
                la.eqanalyte,
                lr.final_result 
            FROM
                lims_results lr
                LEFT JOIN lims_orders lo ON lr.ordno = lo.ordno
                LEFT JOIN lims_analytes la ON ( lr.testcode = la.testcode AND lr.method = la.method AND lr.analyte = la.analyte ) 
            WHERE
                lr.runno = "{runno}"  
            ORDER BY
                lo.ordno,
                la.sorter
                """
        self.curse.execute(sql)
        self.connt.commit()
        rst = self.curse.fetchall()
        return rst

    def count_by_method(self, method, analyte):
        """
        查询某一方法下某一分析项的数量
        :param method: 标准号
        :param analyte: 分析项
        :return:
        """
        sql = f"""
        SELECT
            COUNT(*)
        FROM
            `dbs_lims2_release`.`lims_results` 
        WHERE
            `method` = "{method}" 
            AND `analyte` = "{analyte}" 
            AND `dateenterend` > '2022-12-30 00:00:00' 
        """
        self.curse.execute(sql)
        self.connt.commit()
        rst = self.curse.fetchone()[0]
        return rst


def searchlims(testno='', byno: str = '') -> tuple[tuple[Any, ...], ...]:
    """
    查询sql,
    :param testno: 测试编码
    :param byno: 项目编号或样品编号或批号
    :return:
    """
    db = Limsdb()
    if byno[0].isdigit():  # 批号首位数是数字
        rst = db.search_by_runno(byno)
    else:
        if len(byno) == 9:  # 9位数是样品编号
            byno = db.searchrasprojectno(byno)  # 改成项目编号
        rst = db.search_by_projectno(testno, byno)
    db.close()
    return rst


def count_by_method(method, analyte):
    db = Limsdb()
    count = db.count_by_method(method, analyte)
    db.close()
    return count


def gentmp(rst, filename):
    """
    生成谱图读取通用模板的内容
    :param rst: 查询出的结果
    :param filename: 要保存的excel文件名
    :return:
    """
    #  写入excel
    app = xlwings.App(visible=False, add_book=False)
    file: Book = app.books.add()
    sht: Sheet = file.sheets[0]
    sht.range('a1').value = ['样品编号', '分析项名', '仪器分析项名', '结果', '分组']
    sht.range('a2').value = rst
    #  设置格式
    sht.autofit()  # 自动列宽
    sht.api.Range("A1").AutoFilter(Field=1)  # 首行筛选
    allcell = sht.range('a1').expand()  # 所有单元格
    allcell.api.HorizontalAlignment = -4108  # -4108 水平居中。 -4131 靠左，-4152 靠右。
    for i in range(7, 13):  # 全边框
        allcell.api.Borders(i).LineStyle = 1
        allcell.api.Borders(i).Weight = 2
    # 每间隔一个样品编号，设置底色
    oss = sht.range('a1').expand('down').value  # 所有样品编号带重复
    os = list(set(oss))  # 所有样品编号不重复
    oindexs = [oss.index(o) + 1 for o in os]  # 每个样品编号所在的行号,索引对应到excel要+1
    oindexs.sort()
    colorflag = True  # true为填充底色
    for pre, next_ in zip(oindexs, oindexs[1:] + [len(oss) + 1]):  # pre,next为上一个编号和下一个编号所在的行
        if colorflag:
            sht.range(f'a{pre}:d{next_ - 1}').color = 198, 224, 180
        colorflag = False if colorflag else True  # 切换colorflag状态，达到间隔填充效果

    file.save(rf'C:\Users\Administrator\PycharmProjects\mysite\media\gentmp\{filename}')
    file.close()
    app.quit()


if __name__ == '__main__':
    print(count_by_method('GB/T 5750.5-2006 3.2', '样品浓度'))
    # gentmp("VOC_土_36600", "I1232847", '1.xlsx')
