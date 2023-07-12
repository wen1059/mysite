import xlwings
import re
import math
import os


def gendic(sht):
    '''
    生成{机型：{航路：[lepn,...],...}，...}
    :param sht:
    :return:
    '''

    def gen_list(sht):
        '''
        生成（机型，航路，lepn）
        :param sht:
        :return:
        '''
        for i in range(2, 500):
            jx = sht.range('c{}'.format(i)).value
            if jx in ['机型', 'JX', None, '型号']:  # 如果航班号不是None，添加到结果列表
                continue
            if str(jx).isdigit():
                jx = str(int(jx))  # 整数转为字符串
            hl = sht.range('d{}'.format(i)).value
            yield jx, hl

    jx_list = ['738', '320', '321', '333', '7M8', '773', '73G', '332', '789', '788']
    dict_result = {}
    mdd = re.compile(r'.+-(.)')
    for jx, hl in gen_list(sht):
        hl = mdd.search(hl).group(1)
        # hl=hl[-1]
        if jx not in jx_list:
            jx = 'other'
        if jx not in dict_result:  # 如果结果字典里没有，
            dict_result.setdefault(jx, {})
        if hl not in dict_result[jx]:
            dict_result[jx].setdefault(hl, 0)
        dict_result[jx][hl] += 1
    return dict_result



app = xlwings.App(visible=True, add_book=False)  # 待计算文件
for root, _, files in os.walk(r'C:\Users\Administrator\Desktop\噪声桌面\03.01虹桥加目的地\03.03'):
    for filexlsx in files:
        if 'xlsx' in filexlsx and ('~$' not in filexlsx):
            row_flag = 2
            file_sum = app.books.open(os.path.join(root, filexlsx))
            sht_cal = file_sum.sheets[1]
            sht_sum = file_sum.sheets.add(after=file_sum.sheets[-1])
            dic = gendic(sht_cal)
            for jx in dic:
                for hl in dic[jx]:
                    sht_sum.range('a{}'.format(row_flag)).value = [jx, hl, dic[jx][hl]]
                    row_flag += 1
            file_sum.save()
            file_sum.close()
app.quit()