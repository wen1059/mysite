# -*- coding: utf-8 -*-
# date: 2022/6/1
"""
计算绩效，读取分值表，填入由lims导出的工作量表、计算分值*个数，再分成个人表（参照模板新创建）。
"""
import os
import re
import subprocess
import time
import pandas as pd
import pymysql
import xlwings
from xlwings.main import Book, Sheet
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from tqdm import tqdm
from pypinyin import lazy_pinyin
from io import StringIO


class Mysqldb:
    def __init__(self):
        self.con = pymysql.connect(host='localhost',
                                   port=3306,
                                   user='root',
                                   passwd='WenLiang10072518',
                                   database='mysite'
                                   )
        self.curse = self.con.cursor()

    def createtab(self):
        sql = """
        CREATE TABLE `scores` (
        `id` int NOT NULL COMMENT '测试代码',
        `item` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '测试名称',
        `score` float(255,1) DEFAULT NULL COMMENT '单项分值',
        PRIMARY KEY (`id`) USING BTREE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """
        self.curse.execute(sql)
        self.con.commit()

    def select(self, name):
        sql = f'SELECT {name} FROM scores'
        self.curse.execute(sql)
        rst = self.curse.fetchall()
        return rst


def queryscore(name='item, score, multi') -> dict:
    """
    从mysql读取单项分值，取代readscore()
    :param name: 表的字段名,可以是多个，逗号分隔
    :return:{项目：(分值,倍数)}
    """
    print('正在读取分值表')
    db = Mysqldb()
    rst = db.select(name)
    items = [i[0] for i in rst]
    scores = [i[1] for i in rst]
    multis = [i[2] for i in rst]
    scoredict = dict(zip(items, zip(scores, multis)))
    return scoredict


# def readscore(scoretab) -> dict:
#     """
#     从excel读取单项分值表
#     :param scoretab: 附件2—单项工作分值一览表
#     :return:{项目：分值}
#     """
#     scoredict = {}
#     print('正在打开分值表')
#     app = xlwings.App(visible=False, add_book=False)
#     file: Book = app.books.open(scoretab)
#     sht: Sheet
#     for sht in tqdm([file.sheets[0]], desc='读取分值表', colour='green'):  # 读有机、无机、理化等多个sheet ;2022.06.07都放sheet0了。
#         row = 1000  # 读100行，增加项目后适当修改
#         items = sht.range(f'c1:c{row}').options(transpose=True).value  # 项目名称列，现有模板b列要改成lims项目名
#         singlescores = sht.range(f'e1:e{row}').options(transpose=True).value  # 单项分值列
#         scoredict.update(zip(items, singlescores))
#     scoredict.pop(None)
#     app.quit()
#     return scoredict

def download_dayworktab(start_time, end_time):
    """
    从lims下载单日工作表,xlsx格式
    :param start_time: 开始日期
    :param end_time: 结束日期
    :return:
    """
    print('正在下载每日工作量表')
    # 设置下载路径，打开网页
    options_ = webdriver.ChromeOptions()
    # options_.add_argument('--headless')  # 隐藏浏览器窗口，实测隐藏后下载不到文件，改最小化
    prefs = {'download.default_directory': resultdir}
    options_.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options_)
    driver.minimize_window()  # 最小化窗口
    driver.implicitly_wait(5)
    driver.get('http://10.1.1.80:81/lims/')
    # 登录
    username = driver.find_element(By.XPATH, '//*[@id="username"]')
    username.send_keys('wenliang')
    passwd = driver.find_element(By.XPATH, '//*[@id="password"]')
    passwd.send_keys('wenl')
    login = driver.find_element(By.XPATH, '//*[@id="btn_login"]')
    login.click()
    # 批结果查询
    batch_query = driver.find_element(By.XPATH, '//*[@id="9C61A691C8EB47CDB56AAA824394C6E9"]')
    batch_query.click()
    # 切换到iframe"批结果查询"
    iframe1 = driver.find_element(By.XPATH, '//*[@id="iframe_tab_20180313001"]')
    driver.switch_to.frame(iframe1)
    # 点击打印
    primenu = driver.find_element(By.XPATH, '//*[@id="button-1053"]')
    primenu.click()
    # 切换到iframewindow"工作量统计"
    # "批结果查询"和"工作量统计"是主页面下的两个iframe, 所以需要先返回主页面
    driver.switch_to.default_content()
    iframe2 = driver.find_element(By.XPATH, '//*[@id="IFrame_LEVEL1"]')
    driver.switch_to.frame(iframe2)
    # 输入开始和结束时间,查询
    start = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[2]/div[1]/input')
    start.clear()
    start.send_keys(start_time)
    end = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[1]/div[1]/input')
    end.clear()
    end.send_keys(end_time)
    query = driver.find_element(By.XPATH, '//*[@id="fr-btn-SEARCHDATA"]/div')
    query.click()
    time.sleep(5)  # 预留时间等待查询结果, 结果出来后才能点击"输出"按钮
    # 输出excel, 鼠标点击菜单后网页代码才会出现, ActionChains是鼠标操作, 需要perform()提交执行
    export_button = driver.find_element(By.XPATH, '//*[@id="fr-btn-"]/div/em/button')
    actions = ActionChains(driver)
    while True:
        try:  # 系统未加载出查询结果程序会报错,所以try-except继续等待
            actions.move_to_element(export_button).click().perform()  # 点击"输出"按钮,触发一级菜单
            excel = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]')
            break
        except:
            pass
    actions.move_to_element(excel).perform()  # 移动到"excel",触发二级菜单
    excel2 = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[1]')
    actions.move_to_element(excel2).click().perform()  # 点击二级菜单"原样导出"
    time.sleep(3)  # 预留时间下载excel


def finddayworktab(path):
    """
    查找下载的单日工作表的名称
    :return:
    """
    regx = re.compile(r'.+-.+-.+-.+-.+\.xlsx')
    for file in os.listdir(path):
        if regx.search(file):
            return os.path.join(path, file)


def calscore(dayworktab, scoredict: dict):
    """
    计算分值，在”每日分析工作量.xlsx“后添加两列
    :param dayworktab:每日分析工作量.xlsx
    :param scoredict: readscore()的返回值
    :return:
    chinese = re.compile(r'[\u4e00-\u9fa5]') #中文字符
    """

    def multi() -> float:
        """
        计算无机倍数
        :return:
        """
        elements = '氢氦锂铍硼碳氮氧氟氖钠镁铝硅磷硫氯氩钾钙钪钛钒铬锰铁钴镍铜锌镓锗砷硒溴氪铷' \
                   '锶钇锆铌钼锝钌铑钯银镉铟锡锑碲碘氙铯钡铪钽钨铼锇铱铂金汞铊铅铋钋砹氡钫镭𬬻𬭊𬭳' \
                   '𬭛𬭶鿏𫟼𬬭鎶鉨𫓧镆鉝镧铈镨钕钷钐铕钆铽镝钬铒铥镱镥锕钍镤铀镎钚镅锔锫锎锿镄钔锘铹'
        regx = re.compile(f'[{elements}]')
        try:
            count = len(regx.findall(note))
        except:
            count = 0
        if item in ['砷汞硒锑铋-水']:
            return count if count else 5
        elif item in ['砷汞硒锑铋_土', '金属-含量-702']:
            return count + 1 if count else 5
        elif item in ['金属-浸出液-702', '金属-浸出液-781', '金属-浸出液-766', '重金属_水_776', '重金属_水_5750',
                      '重金属_水_700']:
            match count:
                case 1 | 2:
                    return 1
                case 3 | 4 | 5:
                    return 1.5
                case 6 | 7 | 8 | 9:
                    return 2
            if count > 9 or count == 0:  # 0表示没有备注做全项
                return 2.5
        elif item in ['重金属-环境', '重金属-有组织', '重金属-无组织']:
            match count:
                case 1 | 2:
                    return 1
                case 3 | 4 | 5:
                    return 4 / 3.5
                case 6 | 7 | 8 | 9:
                    return 4.5 / 3.5
            if count > 9 or count == 0:  # 0表示没有备注做全项
                return 5 / 3.5
        else:
            return 1

    print('正在打开每日工作量表')
    app = xlwings.App(visible=False, add_book=False)
    file: Book = app.books.open(dayworktab)
    sht: Sheet = file.sheets[0]
    row = sht.range('c2').expand('down').rows.count + 1  # 总行数
    sht.range('h2').value = ['分值', '总分值', '倍数']
    for i in tqdm(range(3, row + 1), desc='计算每日分值', colour='green'):  # 从第三行开始
        item = sht.range(f'c{i}').value  # 项目名称
        note = sht.range(f'd{i}').value  # 测试备注
        if item not in scoredict:
            print_(f'  [未找到测试项] {item}')
            sht.range(f'h{i}').value = None  # 清空单项分值，因为运维设了默认值1。
            continue
        sht.range(f'h{i}').value = scoredict[item][0]  # 单项分值填入H列
        if scoredict[item][1]:
            multi_ = multi()
            sht.range(f'i{i}').formula = f'=G{i}*H{i}*{multi_}'  # 个数*分值*倍数填入I列
        else:
            multi_ = None
            sht.range(f'i{i}').formula = f'=G{i}*H{i}'  # 个数*分值填入I列
        sht.range(f'j{i}').value = multi_
    file.save()
    app.quit()


def readdayresult(dayworktab) -> dict:
    """
    读取“每日分析工作量”表
    :param dayworktab: 每日分析工作量.xlsx
    :return: {姓名：[(日期，项目，数量，分值，总分)，...],...}
    """

    def fillnone(lst: list | pd.Series):
        """
        把list中的None值替换成前面的非None值
        用于填满合并单元格导致的None值
        :param lst:
        :return:
        """
        flag = None
        for i in range(len(lst)):
            if pd.notnull(lst[i]):
                flag = lst[i]
            else:
                lst[i] = flag
        return lst

    df = pd.read_excel(dayworktab, sheet_name=0, header=1)
    names = df['分析员']
    dates = df['完成日期']
    dates = fillnone(dates.copy())
    items = df['测试信息']
    counts = df['样品个数']
    scores = df['分值']
    allscores = df['总分值']
    multi = df['倍数']
    global dailydate  # 每日工作量表的日期,用来重命名文件
    firstday = str(dates.iloc[0])[:10].replace('-', '')  # 2022YYDD
    lastday = str(dates.iloc[-2])[5:10].replace('-', '')  # YYDD
    dailydate = firstday + '-' + lastday
    dayresult = {}
    # 组合成（name,(dates, items, counts, scores, allscores)）
    for name, *others in zip(names, dates, items, counts, scores, allscores, multi):
        if str(name) == 'nan':
            continue
        if name not in dayresult:
            dayresult.setdefault(name, [])
        dayresult[name].append(others)
    return dayresult


# def readdayresult2(dayworktab) -> dict:
#     """
#     不用，已被readdayresult()取代
#     读取“每日分析工作量”表
#     :param dayworktab: 每日分析工作量.xlsx
#     :return: {姓名：[(日期，项目，数量，分值，总分)，...],...}
#     """
#
#     def fillnone(lst: list) -> list:
#         """
#         把list中的None值替换成前面的非None值
#         用于填满合并单元格导致的None值
#         :param lst:
#         :return:
#         """
#         flag = None
#         for i in range(len(lst)):
#             if lst[i]:
#                 flag = lst[i]
#                 continue
#             if not lst[i]:
#                 lst[i] = flag
#         return lst
#
#     app = xlwings.App(visible=False, add_book=False)
#     file: Book = app.books.open(dayworktab)
#     sht0: Sheet = file.sheets[0]
#     row = sht0.range('c2').expand('down').rows.count + 1  # 总行数
#     # 按列读取
#     names = sht0.range(f'd3:d{row}').options(transpose=True).value
#     dates = sht0.range(f'a3:a{row}').options(transpose=True).value
#     dates = fillnone(dates)
#     items = sht0.range(f'c3:c{row}').options(transpose=True).value
#     counts = sht0.range(f'f3:f{row}').options(transpose=True).value
#     scores = sht0.range(f'g3:g{row}').options(transpose=True).value
#     allscores = sht0.range(f'h3:h{row}').options(transpose=True).value
#     dayresult = {}
#     # 组合成（name,(dates, items, counts, scores, allscores)）
#     for name, *others in zip(names, dates, items, counts, scores, allscores):
#         if name not in dayresult:
#             dayresult.setdefault(name, [])
#         dayresult[name].append(others)
#     app.quit()
#     return dayresult


def trans_day2personal(dayresult: dict, personaltab):
    """
    将每日工作表填入个人工作表
    :param personaltab: 附件3—个人工作量分值统计表
    :param dayresult:readdayresult()返回值
    :return:None
    """

    def shtsort():
        """
        表格排序，按名字的拼音
        :return:
        """
        shtnames = [i.name for i in file.sheets][1:]
        shtnames.sort(key=lambda x: ''.join(lazy_pinyin(x)))
        for index, name in enumerate(shtnames):
            file.sheets[name].api.Move(After=file.sheets[shtnames[index - 1]].api)
        # for name in shtnames:
        #     file.sheets[name].copy()
        #     file.sheets[name].delete()
        #     file.sheets[-1].name = name

    print('正在打开个人分值表')
    app = xlwings.App(visible=False, add_book=False)
    file: Book = app.books.open(personaltab)
    sht_template: Sheet = file.sheets[0]
    for name in tqdm(dayresult, desc='录入个人分值', colour='green'):
        if name not in [s.name for s in file.sheets]:
            sht_template.copy(name=name)  # 新建个人sheet，内容复制模板
        sht_name: Sheet = file.sheets[name]
        row = sht_name.range('e1').expand('down').rows.count  # 总行数,即'合计分数'所在的行数
        sht_name.range(f'e{row}').value = dayresult[name]  # 写入值
        row += len(dayresult[name])  # 更新'合计分数'所在行
        sht_name.range(f'e{row}').value = '合计分数'
        sht_name.range(f'i{row}').formula = f'=SUM(I1:I{row - 1})'
    shtsort()
    # 打开模板后另存为模板名+日期
    if os.path.exists(savename := personaltab[:-5] + dailydate + '.xlsx'):
        os.remove(savename)
    file.save(savename)
    app.quit()
    return savename  # 新增，为了获取名称返回到前端


def renamedayworktab(dayworktab):
    """
    重命名单日工作量表
    :return:
    """
    if os.path.exists(renamepath := f'lims单日工作量表{dailydate}.xlsx'):
        os.remove(renamepath)
    os.rename(dayworktab, renamepath)


def print_(args):
    """
    # 为前端新增
    重写print，将内容同时写入stringio，以便输出到前台
    :param s:
    :param sio:
    :return:
    """
    print(args)
    sio.write(str(args) + '\n')


def main(start, end):
    global sio  # 为前端新增
    sio = StringIO()  # 为前端新增
    global resultdir  # 结果文件保存的目录
    # resultdir = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'calscore_result')
    resultdir = r"C:\Users\Administrator\PycharmProjects\mysite\media\calresult"
    os.chdir(resultdir)
    scoredict = queryscore()
    download_dayworktab(start, end)
    dayworktab = finddayworktab(resultdir)
    calscore(dayworktab, scoredict)
    dayresult = readdayresult(dayworktab)
    personaltab = '附件3—个人工作量分值统计表.xlsx'
    savename = trans_day2personal(dayresult, personaltab)
    renamedayworktab(dayworktab)
    print_('完成')
    sio.write(savename)  # 为前端新增
    sio.seek(0)  # 为前端新增
    return sio.read()  # 为前端新增，为了获取内容返回到前端，最后一行是文件输出目录，其余是print的内容
    # subprocess.run(f'start {resultdir}', shell=True)


if __name__ == '__main__':
    main('2023-01-01', '2023-02-05')
