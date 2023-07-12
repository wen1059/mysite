import xlwings
import re
import math
import os
import pymysql


class Mysqldb:
    """使用此类需要预先在mysql建立好库和表"""

    def __init__(self):
        self.con = pymysql.connect(host='localhost', user='root', passwd='123456', port=3306,
                                   database='airport_noise')
        self.curse = self.con.cursor()

    def ins_to_tab(self, tab, values):
        """
        写入表，insert语句根据表名和values中元素做调整
        :param tab:要写入的标
        :param values: 需要写入的值，列表形式
        :return:
        """
        sql = '''INSERT INTO {} ( pri, 点位, N1, N2, N3, Lamaxpb, Lwecpn, 记录时间 ) VALUES 
            (NULL, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', now())'''.format(
            tab, values[0], values[1], values[2], values[3], values[4], values[5])
        self.curse.execute(sql)
        self.con.commit()

    def cleartab(self):
        """
        清空表
        :return:
        """
        sql = r'TRUNCATE week'
        self.curse.execute(sql)
        self.con.commit()


def yieldsht(walkpath):
    """
    生成每个要处理的表
    :return:
    """
    app_24 = xlwings.App(visible=True, add_book=False)  # 待计算文件
    for root, _, files in os.walk(walkpath):
        for filexlsx in files:
            # if filexlsx in ['航班表.xlsx', '结果.xlsx']:
            #     continue
            if 'xlsx' in filexlsx and ('~$' not in filexlsx):
                file24path = os.path.join(root, filexlsx)
                file24 = app_24.books.open(file24path)  # 24小时文件
                # shtcount = file24.sheets.count  # sheet数量
                # for sc in range(shtcount):
                #     sht = file24.sheets[sc]  # sht：其中一天的sheet
                yield file24.name, file24.sheets[0]
                file24.close()
    app_24.quit()


def count_hb(sht, hb):
    """
    统计3个时间段航班数，更新方法，由行数判断改成根据时间判断
    若要计算周平均，将hb作为函数参数，并去掉return
    :return:
    """
    hour = None
    regx = re.compile(r' (.+?):..')
    for i in range(3, 1823):
        if sht.range('a{}'.format(i)).value == '监测开始时间':
            hour_flag = i + 1
            hour_rex = regx.search(str(sht.range('a{}'.format(hour_flag)).value))
            hour = int(hour_rex.group(1))
        if sht.range('h{}'.format(i)).value not in [None, '起降']:
            if 7 <= hour < 19:
                hb['day'] += 1
            elif 19 <= hour < 22:
                hb['dust'] += 1
            elif 22 <= hour < 24 or 0 <= hour < 7:
                hb['night'] += 1
            # else:
            #     print('\t', file24name, '第{}行：时间格式不正确'.format(i))


def gen_list(sht):
    """
    从excel读取生成（maxla,lepn,td,机型，航路，背景）
    :param sht:
    :return:
    """
    # bg = None
    # mdd = re.compile(r'.+-(.+)')  # 航路取目的地值，按需修改
    for i in range(3, 1647):
        jx = sht.range('h{}'.format(i)).value
        if jx in [None,'起降']:  # 以机型为识别，跳过没有数值的行。
            continue
        # if jx == '机型':  # 更新背景值，背景值在k列“机型”字段的上两行
        #     bg = sht.range('k{}'.format(i - 2)).value
        #     continue
        # if str(jx).isdigit():
        #     jx = str(int(jx))  # 机型转为整数字符串
        hl = sht.range('j{}'.format(i)).value
        # hl = mdd.search(hl).group(1)
        lepn = sht.range('d{}'.format(i)).value
        maxla = sht.range('c{}'.format(i)).value
        td = sht.range('e{}'.format(i)).value
        # print(i, jx, hl, lepn, bg, maxla)
        yield maxla, lepn, td, jx, hl


def gendic(sht,dict_result):
    """
    生成{机型：{航路：[maxlap]...
    若要计算周平均，将dict_result作为函数参数，并去掉return
    :param sht:
    :return:
    """
    # jx_list = ['738', '320', '321', '333', '7M8', '773', '73G', '332', '789', '788']
    for maxla, lepn, td, jx, hl in gen_list(sht):
        # if jx not in jx_list:
        #     jx = 'other'
        if jx not in dict_result:  # 如果结果字典里没有，
            dict_result.setdefault(jx, {})
        if hl not in dict_result[jx]:  # 如果二级字典，某机型的航路没有
            dict_result[jx].setdefault(hl, [])
        # dict_result[jx][hl]['10db'].append(lepn)  # 10db的lepn，用来算比例
        if maxla is None:
            continue
        dict_result[jx][hl].append(maxlap := maxla + 10 * math.log10(td / 20))  # 添加由lamax和td计算得到的l’amax


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
    # print('0的n次方列表求和:',sum10n)
    result = 10 * math.log10(sum10n / len(maxlalist))  # 结果
    return round(result, 1)


def cal_lwecpn_week(lamaxpb, hb):
    return round(lamaxpb + 10 * math.log10((hb['day'] + 3 * hb['dust'] + 10 * hb['night']) / 7) - 27,1)


# def cal_lepn_bar(lepn_bar_result, hbs10_all):
#     """
#     公式2，计算一天的lepnb
#     :param lepn_bar_result:
#     :param hbs10_all:
#     :return:
#     """
#     if len(lepn_bar_result) == 0:
#         return 0
#     sumtlist = list(hbs_10 * math.pow(10, 0.1 * lepnk) for lepnk, hbs_10 in lepn_bar_result)
#     sum_t = math.fsum(sumtlist)
#     result = 10 * math.log10(sum_t / hbs10_all)
#     return round(result, 1)


def run_week(walkpath):
    """
    主程序入口，读取excel，计算，写入mysql
    :param walkpath: os.walk目录
    :return:
    """
    db = Mysqldb()
    # db.cleartab()
    hb = {'day': 0, 'dust': 0, 'night': 0}
    dic={}
    lamaxp_all = []
    file24name=''
    for file24name, sht in yieldsht(walkpath):
        count_hb(sht, hb)
        gendic(sht,dic)
        for jx in dic:
            for hl in dic[jx]:
                lamaxp_part = dic[jx][hl]
                lamaxp_all.extend(lamaxp_part)
    print(hb)
    lamaxpb = cal_bar(lamaxp_all)
    print(lamaxpb)
    lwecpn = cal_lwecpn_week(lamaxpb, hb)
    print(lwecpn)
    sumresult = [dw := (lambda x: re.search(r'(\d{1,2})#(\d{2,4})', x).group(1))(file24name),
                 hb['day'], hb['dust'], hb['night'], lamaxpb, lwecpn]
    db.ins_to_tab('week', sumresult)


if __name__ == '__main__':
    for i in [18,19,53,58,59]:
        path=r"C:\Users\Administrator\Desktop\噪声桌面\复算\{}".format(i)
        run_week(path)
