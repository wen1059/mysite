import xlwings
import re
import math
import os
import pymysql


class Mysqldb:
    def __init__(self):
        self.con = pymysql.connect(host='10.1.210.117', user='root', passwd='123456', port=3306,
                                   database='airport_noise')
        self.curse = self.con.cursor()

    def ins_to_tab(self, values):
        sql = '''INSERT INTO test ( pri, 点位, 日期, 机型, 目的地, 10db架次, 20db架次, lepnk, 记录时间 ) 
            VALUES (NULL, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', now())'''.format(
            values[0], values[1], values[2], values[3], values[4], values[5], values[6])
        self.curse.execute(sql)
        self.con.commit()

    def cleartab(self):
        sql = r'TRUNCATE test'
        self.curse.execute(sql)
        self.con.commit()


def yieldsht():
    app_24 = xlwings.App(visible=True, add_book=False)  # 待计算文件
    for root, _, files in os.walk(r'C:\Users\Administrator\Desktop\噪声桌面\03.01虹桥加目的地\03.03'):
        for filexlsx in files:
            if filexlsx in ['航班表.xlsx', '结果.xlsx']:
                continue
            if 'xlsx' in filexlsx and ('~$' not in filexlsx):
                file24path = os.path.join(root, filexlsx)
                file24 = app_24.books.open(file24path)  # 24小时文件
                shtcount = file24.sheets.count  # sheet数量
                for sc in range(shtcount):
                    sht = file24.sheets[sc]  # sht：其中一天的sheet
                    yield file24.name, sht
                file24.close()
    app_24.quit()


def gen_list(sht):
    """
    生成（机型，航路，lepn）
    :param sht:
    :return:
    """
    bgflag = None
    mdd = re.compile(r'.+-(.+)')
    for i in range(4, 600):
        bg = sht.range('q{}'.format(i)).value
        if bg is not None:
            bgflag = bg
        else:
            bg = bgflag
        jx = sht.range('n{}'.format(i)).value
        if jx in ['机型', 'JX', None, '型号']:  # 如果航班号不是None，添加到结果列表
            continue
        if str(jx).isdigit():
            jx = str(int(jx))  # 整数转为字符串
        hl = sht.range('r{}'.format(i)).value
        hl = mdd.search(hl).group(1)
        lepn = sht.range('d{}'.format(i)).value
        maxla = sht.range('h{}'.format(i)).value
        # print(i, jx, hl, lepn, bg, maxla)
        yield jx, hl, lepn, bg, maxla


def gendic(sht):
    """
    生成{机型：{航路：[[10lepn,...],[20lepn,...]],...}，...}
    :param sht:
    :return:
    """
    jx_list = ['738', '320', '321', '333', '7M8', '773', '73G', '332', '789', '788']
    dict_result = {}
    for jx, hl, lepn, bg, maxla in gen_list(sht):
        if jx not in jx_list:
            jx = 'other'
        if jx not in dict_result:  # 如果结果字典里没有，
            dict_result.setdefault(jx, {})
        if hl not in dict_result[jx]:  # 如果二级字典，某机型的航路没有
            dict_result[jx].setdefault(hl, [[], []])
        dict_result[jx][hl][0].append(lepn)  # 0是10dblepn，用来算比例
        if maxla - bg > 20:
            dict_result[jx][hl][1].append(lepn)
    return dict_result


def cal_lepnk_bar(lepnlist):
    """
    计算lepn平均
    :param lepnlist:
    :return:
    """
    if len(lepnlist) == 0:
        return 0
    sum10nlist = list(math.pow(10, 0.1 * x) for x in lepnlist)  # 10的n次方列表
    sum10n = math.fsum(sum10nlist)  # 10的n次方列表求和
    # print('0的n次方列表求和:',sum10n)
    result = 10 * math.log10(sum10n / len(sum10nlist))  # 结果
    return round(result, 1)


def cal_lepn_bar(lepn_bar_result, hbs10_all):
    if len(lepn_bar_result) == 0:
        return 0
    sumtlist = list(hbs_10 * math.pow(10, 0.1 * lepnk) for lepnk, hbs_10 in lepn_bar_result)
    sum_t = math.fsum(sumtlist)
    result = 10 * math.log10(sum_t / hbs10_all)
    return round(result, 1)


def run():
    db = Mysqldb()
    # db.cleartab()
    for file24name, sht in yieldsht():
        dic = gendic(sht)
        hbs10_all = 0  # 10db架次总数，占比分母
        lepn_bar_result = []  # 用来计算公式3一天的lepn平均
        for jx in dic:
            for hl in dic[jx]:
                lepn_list = dic[jx][hl]
                lepnk_bar = cal_lepnk_bar(lepn_list[1])  # 1是20db的值
                hbs_10 = len(lepn_list[0])  # 10db的识别架次，占比分子
                hbs_20 = len(lepn_list[1])  # 20db的识别架次，仅显示，不参与计算
                hbs10_all += hbs_10
                lepn_bar_result.append((lepnk_bar, hbs_10))
                sumresult = [file24name, str(sht.name), jx, hl, hbs_10, hbs_20, lepnk_bar]
                db.ins_to_tab(sumresult)  # 写入lepnk行
        db.ins_to_tab([''] * 6 + [cal_lepn_bar(lepn_bar_result, hbs10_all)])  # 写入一天的lepn平均行


if __name__ == '__main__':
    run()
