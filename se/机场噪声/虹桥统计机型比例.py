import xlwings
# import re
# import math
import os


def xl_open(filesum_path):
    '''
    创建xlwins实例
    :param filesum_path: 结果文件的路径
    :return:
    '''

    app_sum = xlwings.App(visible=True, add_book=False)  # 结果汇总
    file_sum = app_sum.books.open(filesum_path)
    sht_sum = file_sum.sheets.add(after=file_sum.sheets[-1])  # 每次计算新建一个sheet放最后
    sht_sum.range('a1').value = file_sum.sheets[0].range('a1', 'f1').value  # 复制第一行到新sheet
    return file_sum, sht_sum


def getsht(path):
    '''
    yield （excel文件，sheet）
    :param path: 待处理文件路径
    :return:
    '''
    app_24 = xlwings.App(visible=False, add_book=False)  # 待计算文件
    for root, _, files in os.walk(path):
        for filexlsx in files:
            if 'xlsx' in filexlsx and ('~$' not in filexlsx):
                file24path = os.path.join(root, filexlsx)
                file24 = app_24.books.open(file24path)  # 24小时文件
                shtcount = file24.sheets.count  # sheet数量
                for sc in range(shtcount):
                    sht = file24.sheets[sc]  # sht：其中一天的sheet
                    yield file24, sht
                file24.close()
                try:
                    os.remove(file24path)
                except:
                    pass
    app_24.quit()


def gen_list(sht):
    '''
    生成机型
    :param sht: 当前处理的sheet
    :return:结果列表
    '''
    # list_result = []
    for i in range(1, 600):
        # hbh = sht.range('m{}'.format(i)).value  # 航班号
        jx = sht.range('n{}'.format(i)).value  # 机型
        # zip_hbh_jx = (hbh, jx)
        if jx not in ['机型', 'JX', None, '型号']:  # 如果航班号不是None，添加到结果列表
            if str(jx).isdigit():
                jx = str(int(jx))  # 整数转为字符串
            yield jx
            # list_result.append(jx)
    # return list_result


def count_jx(sht):
    '''
    生成字典{机型：数量}
    :param sht: 当前处理的sheet
    :return:结果字典
    '''
    jx_list = ['738', '320', '321', '333', '7M8', '773', '73G', '332', '789', '788']
    list_result = gen_list(sht)
    dict_result = {'其他': 0}
    for jx in list_result:
        # jx = jx[1]
        if jx not in dict_result:  # 如果结果字典里没有，
            if jx in jx_list:  # 如果在jx_list
                dict_result.setdefault(jx, 1)  # 添加这个航班号，次数是1
            else:
                dict_result['其他'] += 1  # 数量算在其他里
        else:  # 如果已经有航班号，次数+1
            dict_result[jx] += 1
    return dict_result


def run():
    def sum_result():
        cishu = dict_result[jx]  # 次数
        sum_cishu = sum(dict_result.values())  # 次数总和
        bili = cishu / sum_cishu if sum_cishu != 0 else 0  # 比例
        sum_result = [file24.name, str(sht.name), jx, file24.name + str(sht.name) + str(jx), cishu,
                      round(bili * 100, 1)]
        return sum_result

    file_sum, sht_sum = xl_open(r'C:\Users\Administrator\Desktop\噪声桌面\计算结果\虹桥统计机型.xlsx')
    row_flag = 2  # sht_sum从第二行开始填数值
    for file24, sht in getsht(r'C:\Users\Administrator\Desktop\噪声桌面\待计算'):
        dict_result = count_jx(sht)
        # print(dict_result)
        for jx in dict_result:
            sht_sum.range('a{}'.format(row_flag)).value = sum_result()
            row_flag += 1
        row_flag += 1  # 不同天之间加空格
    file_sum.save()
    # sht_sum.range('a{}'.format(row_flag)).value = '-' * 100 + ' 点位分割线 ' + '-' * 100
    # row_flag += 1


if __name__ == '__main__':
    run()
