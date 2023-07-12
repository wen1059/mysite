import xlwings
import re
import math
import os

app = xlwings.App(visible=True, add_book=False)  # 待计算文件
app_sum = xlwings.App(visible=True, add_book=False)  # 结果汇总
file_sum = app_sum.books.open(r"C:\Users\Administrator\Desktop\噪声桌面\03.01虹桥加目的地\0303大于20db的单日lepn平均值.xlsx")
sht_sum = file_sum.sheets.add(after=file_sum.sheets[-1])
sht_sum.range('a1').value = file_sum.sheets[0].range('a1', 'j1').value
row_flag = 2


def counthb(rng):
    regx = re.compile(r' (..):..')
    hour = regx.search(rng)
    # print('hour:',hour)
    try:
        hour = int(hour.group(1))
    except Exception as ef:
        print('counthb()1', ef, '时间不是数字')
    else:
        if 7 <= hour < 19:
            hbdict['day'] += 1
        elif 19 <= hour < 22:
            hbdict['dust'] += 1
        elif 22 <= hour < 24 or 0 <= hour < 7:
            hbdict['night'] += 1
        else:
            print('counthb()2', '时间格式不正确')


def cal_lepn_10db():
    if len(lepnlist) == 0:
        return 0
    sum10nlist = list(math.pow(10, (x / 10)) for x in lepnlist)  # 10的n次方列表
    sum10n = math.fsum(sum10nlist)  # 10的n次方列表求和
    # print('0的n次方列表求和:',sum10n)
    o_n = 1 / len(sum10nlist)  # 1/N
    # print('N:',len(sum10nlist))
    result = 10 * math.log10(o_n * sum10n)  # 结果
    return round(result, 1)


for root, _, files in os.walk(r'C:\Users\Administrator\Desktop\噪声桌面\03.01虹桥加目的地\03.03'):
    for filexlsx in files:
        if 'xlsx' in filexlsx and ('~$' not in filexlsx):
            file = app.books.open(os.path.join(root, filexlsx))
            shtcount = file.sheets.count
            for sc in range(shtcount):
                sht = file.sheets[sc]
                lepnlist = []
                hbdict = {'day': 0, 'dust': 0, 'night': 0}
                bgflag = None
                for row in range(4, 700):
                    lepnvalue = sht.range('d{}'.format(row)).value
                    maxla = sht.range('h{}'.format(row)).value
                    bg = sht.range('q{}'.format(row)).value
                    if bg is not None:
                        bgflag = bg
                    else:
                        bg = bgflag
                    # print('lepnvalue:',lepnvalue)
                    if not lepnvalue:
                        continue
                    try:
                        int(lepnvalue)
                    except Exception as e:
                        # print('int(lepnvalue)', e)
                        continue
                    try:
                        lepnvalue - bg
                    except:
                        print(row)
                    if lepnvalue > 50 and maxla - bg > 20:
                        lepnlist.append(lepnvalue)
                        counthb(str(sht.range('a{}'.format(row)).value))
                lepnresult = cal_lepn_10db()
                # print(lepnresult)
                try:
                    lwecpn_10db = round(
                        lepnresult + 10 * math.log10(hbdict['day'] + 3 * hbdict['dust'] + 10 * hbdict['night']) - 39.4,
                        1)
                except Exception as e:
                    # print(e)
                    lwecpn_10db = 0
                xlresult = [hbdict['day'], hbdict['dust'], hbdict['night'], math.fsum(hbdict.values()), None,
                            lepnresult, None, lwecpn_10db]
                sht.range('c2').value = xlresult
                sht_sum.range('a{}'.format(row_flag)).value = [file.name, str(sht.name)] + xlresult
                row_flag += 1
            file_sum.save()
            file.close()
            # os.remove(os.path.join(root, filexlsx))
app.quit()
