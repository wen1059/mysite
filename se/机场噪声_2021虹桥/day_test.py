"""
2021.04.14更新，将单日和周平均合并，week.py不再使用
04.17更新，lwecpn_20db计算的航班由所有航班改为20db航班，新增lwecpn_all计算，用原来所有航班
04.19修改，适用于精密法，使用lepn计算。
"""
import math
import os
import re
import pymysql
import xlwings
import time
import shutil
from decimal import Decimal


class Mysqldb:
    """使用此类需要预先在mysql建立好库和表"""

    def __init__(self):
        self.con = pymysql.connect(host='localhost',
                                   port=3306,
                                   user='root',
                                   passwd='123456',
                                   database='airport_noise'
                                   )
        self.curse = self.con.cursor()

    def createtab(self):
        """
        建立表，预留备用
        :return:
        """
        sql = '''
            CREATE TABLE `day_acu` (
              `pri` int NOT NULL AUTO_INCREMENT,
              `点位` varchar(255) DEFAULT NULL,
              `日期` varchar(255) DEFAULT NULL,
              `分析员` varchar(255) DEFAULT NULL,
              `N1` int DEFAULT NULL,
              `N2` int DEFAULT NULL,
              `N3` int DEFAULT NULL,
              `N总` int DEFAULT NULL,
              `Lamaxpb` float(255,1) DEFAULT NULL,
              `Lwecpn` float(255,1) DEFAULT NULL,
              `N1_20` int DEFAULT NULL,
              `N2_20` int DEFAULT NULL,
              `N3_20` int DEFAULT NULL,
              `N总_20` int DEFAULT NULL,
              `Lamaxpb_20` float(255,1) DEFAULT NULL,
              `Lwecpn_20` float(255,1) DEFAULT NULL,
              `Lwecpn_N总20` float(255,1) DEFAULT NULL,
              `背景` float(255,1) DEFAULT NULL,
              `记录时间` datetime DEFAULT NULL,
              PRIMARY KEY (`pri`)
            ) ENGINE=InnoDB AUTO_INCREMENT=1387 DEFAULT CHARSET=utf8;
            '''
        self.curse.execute(sql)
        self.con.commit()

    def ins_to_tab(self, tab, values):
        """
        写入表，insert语句根据表名和values中元素做调整
        :param tab:要写入的表
        :param values: 需要写入的值，列表形式
        :return:
        """
        sql = '''INSERT INTO {} 
            ( pri, 点位, 日期, 分析员, N1, N2, N3, N总, Lamaxpb, Lwecpn, 
            N1_20, N2_20, N3_20, N总_20, Lamaxpb_20, Lwecpn_20, Lwecpn_N总20, 背景, 记录时间 ) 
            VALUES (NULL, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', 
            \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', now())''' \
            .format(tab, values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7],
                    values[8], values[9], values[10], values[11], values[12], values[13], values[14], values[15],
                    values[16])
        self.curse.execute(sql)
        self.con.commit()

    def cleartab(self, tab):
        """
        清空表
        :return:
        """
        sql = r'TRUNCATE {}'.format(tab)
        self.curse.execute(sql)
        self.con.commit()


def yieldsht(walkpath):
    """
    生成每个要处理的表
    :return:
    """
    # app_24 = xlwings.App(visible=False, add_book=False)  # 待计算文件
    for root, _, files in os.walk(walkpath):
        for filexlsx in files:
            if filexlsx[-5:-1] != '.xls' or '~$' in filexlsx:
                continue
            file24path = os.path.join(root, filexlsx)
            file24 = app_24.books.open(file24path)  # 24小时文件
            # shtcount = file24.sheets.count  # sheet数量
            # for sc in range(shtcount):
            #     sht = file24.sheets[sc]  # sht：其中一天的sheet
            yield file24.name, file24.sheets[0]
            file24.close()
            shutil.copy(file24path, r"C:\Users\Administrator\Desktop\虹桥噪声桌面\计算备份\{}".format(
                time.strftime('%H_%M_%S', time.localtime(time.time())) + '_' + filexlsx))  # 新增备份功能
            os.remove(file24path)
    # app_24.kill()


def count_hb(sht):
    """
    统计3个时间段航班数，更新方法，由行数判断改成根据时间判断
    04.17更新，同时统计所有的和>20db的
    :param sht:
    :return:
    """

    def count_inner(hb):
        if 7 <= hour < 19:
            hb['day'] += 1
        elif 19 <= hour < 22:
            hb['dust'] += 1
        elif 22 <= hour < 24 or 0 <= hour < 7:
            hb['night'] += 1

    hb_all = {'day': 0, 'dust': 0, 'night': 0}
    hb_20 = hb_all.copy()
    hour = None
    regx = re.compile(r' (\d{1,2}):..')
    for i in range(3, 2080):
        if sht.range('a{}'.format(i)).value == '监测开始时间':
            hour_rex = regx.search(str(sht.range('a{}'.format(i + 1)).value))
            hour = int(hour_rex.group(1))
            # print(hour)
        if sht.range('j{}'.format(i)).value in [None, '机型']:  # 值对应机型列,如果有事件，统计架次
            continue
        count_inner(hb_all)  # 统计所有,<20db和温湿度剔除项都统计在内
        # ---------4.17更新，统计lamax>20的，即在[lamaxp_all_day]中的航班的架次
        bg = float(sht.range('n4').value)
        maxla = sht.range('h{}'.format(i)).value
        if maxla is None:  # none表示背景干扰，赋值100以满足maxla - bg > 20，仅表示参与统计，此函数不影响数值计算
            maxla = 100
        # td = sht.range('e{}'.format(i)).value
        if maxla - bg > 20.01:  # and td > 1.5:
            count_inner(hb_20)  # 统计>20db
        # ---------
    return hb_all, hb_20


def gen_list(sht):
    """
    从excel读取生成（maxla,lepn,td,机型，航路，背景,是否剔除）
    由机型判断，生成有机型的行
    :param sht:
    :return:
    """
    bg, eli = None, None  # eli是剔除项，Ture的时候是剔除
    # mdd = re.compile(r'.+-(.+)')  # 航路取目的地值，按需修改
    for i in range(3, 2080):
        jx = sht.range('j{}'.format(i)).value
        if jx is None:  # 以机型为识别，跳过没有数值的行。
            continue
        if jx == '机型':  # 更新背景值，背景值在k列“机型”字段的上两行
            bg = float(sht.range('n4').value)  # sht.range('k{}'.format(i - 2)).value # 4.17更新，背景只取k4格
            eli = sht.range('p{}'.format(i - 2)).value
            continue
        if str(jx).isdigit():
            jx = str(int(jx))  # 机型转为整数字符串,因为xlwings读出来的数字是浮点数
        hl = sht.range('n{}'.format(i)).value
        # hl = mdd.search(hl).group(1) #航路改为英文字母，此条不再有用
        lepn = sht.range('d{}'.format(i)).value
        maxla = sht.range('h{}'.format(i)).value
        td = sht.range('e{}'.format(i)).value
        yield maxla, lepn, td, jx, hl, bg, eli


def gendic(sht):
    """
    生成{机型：{航路：[maxlap]...
    若要计算周平均，将dict_result作为函数参数，并去掉return
    2021.4.12新更新把剔除的和正常的分开放
    04.17更新，同时生成所有的和>20db的
    :param sht:
    :return:
    """
    dic_all, dic_20 = {}, {}

    def gendic_inner(dic):
        if jx not in dic:  # 如果结果字典里没有机型，
            dic.setdefault(jx, {})
        if hl not in dic[jx]:  # 如果二级字典，某机型没有航路
            dic[jx].setdefault(hl, {'nor': [], 'eli': []})
        # maxlap = maxla + 10 * math.log10(td / 20)  # lamax和td计算得到的l’amax
        maxlap = lepn  # 更新，由maxlap改为lepn，变量名没有改。
        if eli == 1:
            dic[jx][hl]['eli'].append(maxlap)
        else:
            dic[jx][hl]['nor'].append(maxlap)

    for maxla, lepn, td, jx, hl, bg, eli in gen_list(sht):
        if maxla is None:  # or td == 1.5:  # 04.17更新，td1.5的数值不纳入计算，这样不用再在谱图上删
            continue  # 如果“背景干扰/跨时段”or "td=1.5"，不添加进字典
        gendic_inner(dic_all)  # 所有添加到dic_all
        if maxla - bg > 20.01:  # 如果大于20db，另外添加一份到dic_20
            gendic_inner(dic_20)
    return dic_all, dic_20


def gendic_addmax(dic):
    """
    2021.4.12新更新，每个层级添加max值这一项如{jx1：{hl1:{{...},max:_},hl2:{}, max:_}， jx2：{...}， max：_}
    :param dic:
    :return:
    """
    # 添加max
    if dic == {}:
        return dic
    dicmaxlst = []  # 第一层，整个字典,所有机型max
    for jx in dic:
        jxmaxlst = []  # 第二层，某机型max
        for hl in dic[jx]:
            print(jx,hl,dic[jx][hl]['nor'])
            max_nor = max(dic[jx][hl]['nor']) if dic[jx][hl]['nor'] else 0  # 第三层，某机型，某航路的max
            dic[jx][hl].setdefault('max', max_nor)
            jxmaxlst.append(max_nor)  # 添加到列表，用来算第二层max
        max_jx = max(jxmaxlst)
        dic[jx].setdefault('max', max_jx)
        dicmaxlst.append(max_jx)  # 添加到列表，用来算第一层max
    max_dic = max(dicmaxlst)
    dic.setdefault('max', max_dic)
    return dic


def searchmax(dic, jx, hl):
    """
    找到字典里的max值
    规则：先找同机型同航路，如果没有找同机型，如果没有找所有机型
    :param dic:
    :param jx:
    :param hl:
    :return:
    """
    if max_lp := dic[jx][hl]['max']:
        return max_lp
    elif max_lp := dic[jx]['max']:
        return max_lp
    else:
        return dic['max']


def gen_lamaxp_all(dic):
    """
    将按机型航路分开的lamax‘合并到一起
    后续因不满足气象条件要替换的功能也写到这里(2021.04.12已添加)
    :param dic:
    :return:
    """
    lamaxp_all = []
    for jx in dic:
        if jx == 'max':
            continue
        for hl in dic[jx]:
            if hl == 'max':
                continue
            lamaxp_part = dic[jx][hl]['nor']
            lamaxp_all.extend(lamaxp_part)
            if not dic[jx][hl]['eli']:
                continue
            max_lp = searchmax(dic, jx, hl)
            lamaxp_all.extend([max_lp] * len(dic[jx][hl]['eli']))
    return lamaxp_all


def cal_bar(maxlalist):
    """
    计算lepn或lamaxp平均
    :param maxlalist:lepn或lamaxp的列表
    :return:
    """
    if len(maxlalist) == 0:
        return 0
    sum10nlist = list(math.pow(10, 0.1 * x) for x in maxlalist)  # 10的n次方列表
    sum10n = math.fsum(sum10nlist)  # 10的n次方列表求和
    result = 10 * math.log10(sum10n / len(maxlalist))  # 结果
    # return round(result,1)
    return float(Decimal(f'{result}').quantize(Decimal('0.0')))


def cal_lwecpn(lamaxpb, hb):
    """
    计算单日lwecpn
    总架次/7后用于计算周平均
    :param lamaxpb:
    :param hb:
    :return:
    """
    if sum(hb.values()) == 0:
        return 0
    result = lamaxpb + 10 * math.log10(hb['day'] + 3 * hb['dust'] + 10 * hb['night']) - 39.4
    # return round(result, 1)
    return float(Decimal(f'{result}').quantize(Decimal('0.0')))


def cal_oneday_week(walkpath):
    """
    核心功能程序，计算
    2021.04.14更新，分割线内是原本的单日计算，外部是合并的cal_week2周计算，合并计算后不用读取excel两次
    04.17更新，同时计算所有的和大于20db的
    :param walkpath: 一周的os.walk目录
    :return:
    """

    def dw_date(file24name):
        if f24n_re := re.search(r'(\d{1,2}.*)#(\d{2,4})(...)', file24name):
            dianwei, date, fx_name = f24n_re.group(1), f24n_re.group(2), f24n_re.group(3)
            if '精' in fx_name:
                fx_name = fx_name.replace('精', '')
        else:
            dianwei, date, fx_name = '00', '0000', '000'
        return dianwei, date, fx_name

    lamaxp_all_week_20 = []
    hb_week_20 = {'day': 0, 'dust': 0, 'night': 0}
    lamaxp_all_week_all = []
    hb_week_all = hb_week_20.copy()
    dianwei, fx_name = '', ''
    # 这条线内的是单日计算---------------
    for file24name, sht in yieldsht(walkpath):
        dianwei, date, fx_name = dw_date(file24name)
        bg = float(sht.range('n4').value)
        dic_ = gendic(sht)
        hb_ = count_hb(sht)
        # ---以下是>20db的日计算
        dic_day_20 = gendic_addmax(dic_[1])
        lamaxp_all_day_20 = gen_lamaxp_all(dic_day_20)
        lamaxpb_day_20 = cal_bar(lamaxp_all_day_20)
        hb_day_20 = hb_[1]
        lwecpn_day_20 = cal_lwecpn(lamaxpb_day_20, hb_day_20)
        # ---以下是不分20db的日计算
        dic_day_all = gendic_addmax(dic_[0])
        lamaxp_all_day_all = gen_lamaxp_all(dic_day_all)
        lamaxpb_day_all = cal_bar(lamaxp_all_day_all)
        hb_day_all = hb_[0]
        lwecpn_day_all = cal_lwecpn(lamaxpb_day_all, hb_day_all)
        lwecpn_day_n20 = cal_lwecpn(lamaxpb_day_20, hb_day_all)  # 04.23新增用总航班和20db_lepn计算
        sumresult_day = (dianwei + '#', date, fx_name, hb_day_all['day'], hb_day_all['dust'], hb_day_all['night'],
                         sum(hb_day_all.values()), lamaxpb_day_all, lwecpn_day_all, hb_day_20['day'],
                         hb_day_20['dust'], hb_day_20['night'], sum(hb_day_20.values()), lamaxpb_day_20,
                         lwecpn_day_20, lwecpn_day_n20, bg)
        yield sumresult_day
        lamaxp_all_week_20.extend(lamaxp_all_day_20)  # 周计算新加语句
        for i in hb_day_20:  # 周计算新加语句
            hb_week_20[i] += hb_day_20[i] / 7  # 周计算新加语句
        lamaxp_all_week_all.extend(lamaxp_all_day_all)  # 周计算新加语句
        for i in hb_day_all:  # 周计算新加语句
            hb_week_all[i] += hb_day_all[i] / 7  # 周计算新加语句
    # ------------------
    # ---以下是>20db的周计算
    lamaxpb_week_20 = cal_bar(lamaxp_all_week_20)
    lwecpn_week_20 = cal_lwecpn(lamaxpb_week_20, hb_week_20)
    # ---以下是不分20db的周计算
    lamaxpb_week_all = cal_bar(lamaxp_all_week_all)
    lwecpn_week_all = cal_lwecpn(lamaxpb_week_all, hb_week_all)
    lwecpn_week_n20 = cal_lwecpn(lamaxpb_week_20, hb_week_all)  # # 04.23新增用总航班和20db_lepn计算
    sumresult_week = (dianwei + '#', '周平均', fx_name, hb_week_all['day'], hb_week_all['dust'], hb_week_all['night'],
                      sum(hb_week_all.values()), lamaxpb_week_all, lwecpn_week_all, hb_week_20['day'],
                      hb_week_20['dust'], hb_week_20['night'], sum(hb_week_all.values()), lamaxpb_week_20,
                      lwecpn_week_20, lwecpn_week_n20, '')
    yield sumresult_week


def run_oneday_week(walkpath):
    """
    程序入口，写入mysql
    :param walkpath:总目录,得到的下层目录作为yieldsht的os.walk的根目录
    :return:
    """
    # db = Mysqldb()
    # db.cleartab('day')
    # db.cleartab('week')
    for weekwalkpath, _, _ in os.walk(walkpath):
        # if weekwalkpath == walkpath:
        #     continue
        sumresult = list(cal_oneday_week(weekwalkpath))  # 前7个元素是日平均，最后一个是周平均
        # for sumres in sumresult[:-1]:
        # db.ins_to_tab('day_acu', sumres)  # 写入单日结果
        # if len(sumresult) == 8:
        #     db.ins_to_tab('week', sumresult[-1])  # 写入周结果


if __name__ == '__main__':
    app_24 = xlwings.App(visible=False, add_book=False)  # 待计算文件

    run_oneday_week(r"C:\Users\Administrator\Desktop\虹桥噪声桌面\测试")

    # app_24.kill()
