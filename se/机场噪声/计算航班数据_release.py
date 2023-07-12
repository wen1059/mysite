# 此为分发版本，调整了路径为当前路径，结果文件也保存到当前路径
import math
import os
import re
import time

try:
    import xlwings
except ImportError:
    print('第一次运行会安装依赖库，请耐心等待')
    os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple xlwings')
    print('安装完成')
    import xlwings

print('请把此程序放在excel的同级或上级目录\n结果会保存在“计算结果.xlsx”\n请确保已安装Microsoft Excel\n')
dict_bj = {
    '01#': 45.5, '02#': 41.9, '03#': 38.8, '04#': 41.2, '06#': 36.5, '49#': 42.9, '50#': 40.1, '05#': 40.3, '09#': 38.6,
    '51#': 46.2, '07#': 41.9, '10#': 41.6, '08#': 38.7, '11#': 36.6, '12#': 46.4, '13#': 40.4, '52#': 36.2, '65#': 41.1,
    '43#': 40.1, '44#': 45.2, '42#': 43.6, '55#': 37.1, '45#': 42.5, '14#': 37.4, '15#': 44.4, '16#': 45.9,
    '53#': 34.3, '19#': 45.1, '68#': 48.8, '18#': 34.8, '58#': 34.6, '69#': 36.2, '59#': 43.4, '60#': 34.4,
    '67#': 41.7, '61#': 40.9, '64#': 42.1, '62#': 40.7, '63#': 42.1, '17#': 43.6, '46#': 41.6, '47#': 39.7, '70#': 40.4,
    '25#': 44, '27#': 45.9, '28#': 38, '56#': 48.9, '57#': 42,
    '31#': 43.9, '32#': 44, '33#': 46, '35#': 45.9, '36#': 37.9, '37#': 45.5, '38#': 42, '39#': 41.9, '40#': 43.9,
    '41#': 43.9, '66#': 46.5, '71#': 43.4,
    '20#': 44.1, '21#': 40.2, '22#': 41.0, '23#': 44.0, '24#': 43.5, '26#': 40.9, '29#': 42.9, '30#': 43.9, '34#': 42.9,
    '48#': 37.9, '54#': 45.8,
    '72#': 35.6, '73#': 37.2, '74#': 33.2, '75#': 33.5, '76#': 35.8
}
result_flag = 2  # 最终汇总开始行
# calrootpath = os.getcwd()
calrootpath = r"C:\Users\Administrator\Desktop\虹桥噪声桌面\浦东简易法复算lamax"
file_result = None
app1 = xlwings.App(visible=True, add_book=False)  # 结果excel文件
if not os.path.exists('计算结果.xlsx'):
    file_result = app1.books.add()
    file_result.save('计算结果.xlsx')
    file_result.sheets[0].range('a1').value = ['点位', '日期', '白天', '傍晚', '晚上', '总数', 'lepn_10', 'lepn_20', 'lwecpn_10',
                                               'lwecpn_20', '计算时间']
else:
    file_result = app1.books.open(r'计算结果.xlsx')
shtres = file_result.sheets.add(after=file_result.sheets[-1])
shtres.range('a1').value = file_result.sheets[0].range('a1').expand('right').value


def gendic():  # 生成字典 {航班号：（maxLA，Lepn,td）}
    dic_fcd = {}
    for i in range(1, 1824):
        flagval = sht0.range(i, 3).value
        if str(flagval)[0].isdigit() and ('#' not in str(flagval)):
            dic_fcd.setdefault(str(sht0.range(i, 6).value) + str(i),
                               (sht0.range(i, 3).value, sht0.range(i, 4).value, sht0.range(i, 5).value))
    try:
        dic_fcd.pop(None)
    except:
        pass
    return dic_fcd


# def cal_lepn_10db():
#     """
#     lepn计算
#     :return:
#     """
#     sum10nlist = list(math.pow(10, (x[1] / 10)) for x in dic_fcd_values if x[1])  # 10的n次方列表
#     sum10n = math.fsum(sum10nlist)  # 10的n次方列表求和
#     # print('0的n次方列表求和:',sum10n)
#     one_N = 1 / len(sum10nlist)  # 1/N
#     # print('N:',len(sum10nlist))
#     result = 10 * math.log10(one_N * sum10n)  # 结果
#     return result


def cal_lepn_10db():
    """
    lamax计算
    :return:
    """
    lpamax_list = list(x[0] + 10 * math.log10(x[2] / 20) for x in dic_fcd_values if (x[2] and x[0]))
    sum10nlist = list(math.pow(10, (x / 10)) for x in lpamax_list)  # 10的n次方列表
    sum10n = math.fsum(sum10nlist)  # 10的n次方列表求和
    # print('0的n次方列表求和:',sum10n)
    one_N = 1 / len(sum10nlist)  # 1/N
    # print('N:',len(sum10nlist))
    result = 10 * math.log10(one_N * sum10n)  # 结果
    return result


# def cal_lepn_20db_gd(bj):
#     sum20nlist = list(math.pow(10, (x[1] / 10)) for x in dic_fcd_values if (x[1] and x[0] > 20 + bj))
#     sum20n = math.fsum(sum20nlist)
#     # print('10的n次方列表求和:', sum20n)
#     one_N = 1 / len(sum20nlist)
#     # print('N:', len(sum20nlist))
#     result = 10 * math.log10(one_N * sum20n)
#     return result


def cal_lepn_20db_gd(bj):
    lpamax_list = list(x[0] + 10 * math.log10(x[2] / 20) for x in dic_fcd_values if (x[2] and x[0] > 20 + bj))
    sum20nlist = list(math.pow(10, (x / 10)) for x in lpamax_list)
    sum20n = math.fsum(sum20nlist)
    # print('10的n次方列表求和:', sum20n)
    one_N = 1 / len(sum20nlist)
    # print('N:', len(sum20nlist))
    result = 10 * math.log10(one_N * sum20n)
    return result


def count_hb_old():  # 此函数没用了，已被count_hb（）更新
    ct_bt, ct_bw, ct_ws = 0, 0, 0
    for i in range(1, 1823):
        if sht0.range('f{}'.format(i)).value not in [None, '航班号', '航班信息']:
            if 532 < i < 1425:
                ct_bt += 1
            elif 1339 < i < 1653:
                ct_bw += 1
            elif 1659 < i < 1823 or 0 < i < 515:
                ct_ws += 1
    return ct_bt, ct_bw, ct_ws


def count_hb():
    '''
    更新方法，由行数判断改成根据时间判断
    :return:
    '''
    hour = None
    hb = {'day': 0, 'dust': 0, 'night': 0}
    regx = re.compile(r' (.+?):..')
    for i in range(1, 1823):
        if sht0.range('a{}'.format(i)).value == '监测开始时间':
            hour_flag = i + 1
            hour_rex = regx.search(str(sht0.range('a{}'.format(hour_flag)).value))
            hour = int(hour_rex.group(1))
        if sht0.range('f{}'.format(i)).value not in [None, '航班号', '航班信息']:
            if 7 <= hour < 19:
                hb['day'] += 1
            elif 19 <= hour < 22:
                hb['dust'] += 1
            elif 22 <= hour < 24 or 0 <= hour < 7:
                hb['night'] += 1
            else:
                print('\t', filexlsx, '第{}行：时间格式不正确'.format(i))
                errorfile.append(filexlsx)
    return hb


def getdianwei():
    dianwei = filexlsx[0:2]
    if '#' not in dianwei:
        dianwei += '#'
    return dianwei


app2 = xlwings.App(visible=False, add_book=False)  # app2是24小时原始数据
errorfile = []
for root, _, files in os.walk(calrootpath):
    for filexlsx in files:
        if filexlsx == '计算结果.xlsx':
            continue
        if 'xlsx' in filexlsx and ('~$' not in filexlsx):
            print('正在计算{}'.format(filexlsx))
            file24 = app2.books.open(os.path.join(root, filexlsx))
            sht0 = file24.sheets[0]
            if '23:00' not in str(sht0.range('a1793').value):
                print('\t', filexlsx, '文件不是1823行')
            dic_fcd = gendic()
            dic_fcd_values = list(dic_fcd.values())  # 字典value
            try:
                lepn_10db_noround = cal_lepn_10db()
                lepn_10db = round(lepn_10db_noround, 1)
            except Exception as e:
                print('\t1', filexlsx, '未计算成功，请检查文件', e)
                errorfile.append(filexlsx)
                file24.close()
                continue
            dianwei = getdianwei()
            try:
                lepn_20db_norund = cal_lepn_20db_gd(dict_bj[dianwei])
                lepn_20db = round(lepn_20db_norund, 1)
                # print(lepn_20db_norund,lepn_20db)
            except Exception as e:
                # lepn_20db = cal_lepn_20db_gd(dict_bj[(str(sht0.range('c4').value)+'#').replace('.0#','#')])
                print('\t2', filexlsx, '未计算成功，请检查文件', e)
                errorfile.append(filexlsx)
                file24.close()
                continue
            try:
                hb = count_hb()
            except Exception as e:
                print('\t3', filexlsx, '未计算成功，请检查文件', e)
                file24.close()
                continue
            day, dust, night = hb['day'], hb['dust'], hb['night']
            # lwecpn_10db = round(lepn_10db + 10 * math.log10(day + 3 * dust + 10 * night) - 39.4, 1)  # lepn计算
            # lwecpn_20db = round(lepn_20db + 10 * math.log10(day + 3 * dust + 10 * night) - 39.4, 1)  # lepn计算
            lwecpn_10db = round(lepn_10db + 10 * math.log10(day + 3 * dust + 10 * night) - 27, 1)  # lamax计算
            lwecpn_20db = round(lepn_20db + 10 * math.log10(day + 3 * dust + 10 * night) - 27, 1)  # lamax计算
            list_result0 = [dianwei, sht0.range('a4').value, day, dust, night, day + dust + night, lepn_10db, lepn_20db,
                            lwecpn_10db, lwecpn_20db,
                            time.strftime('%Y.%m.%d-%H:%M', time.localtime(time.time()))]
            shtres.range('a{}'.format(result_flag)).value = list_result0
            file_result.save()
            file24.close()
            # os.remove(os.path.join(root, filexlsx))
            result_flag += 1
app2.quit()
if errorfile[0]:
    print('\n有错误的文件：', errorfile)
print('\n全部处理完成，按任意键退出')
input()
