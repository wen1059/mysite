import xlwings, math, os, time ,re

result_flag = 2  # 最终汇总开始行
app1 = xlwings.App(visible=True, add_book=False)
file_result = app1.books.open(r'C:\Users\Administrator\Desktop\噪声桌面\计算结果\calresult.xlsx')
shtres = file_result.sheets.add(after=file_result.sheets[-1])
shtres.range('a1').value = ['点位','日期','La\'Max平均值','Lepn平均值（La\'Max平均值+13）']
app2 = xlwings.App(visible=False, add_book=False)  # app2是24小时原始数据


def gendic():  # 生成字典 {航班号：（maxLA，td）}
    dicFCD = {}
    for i in range(1, 1824):
        flagval = sht0.range(i, 3).value
        if str(flagval)[0].isdigit() and ('#' not in str(flagval)):
            dicFCD.setdefault(str(sht0.range(i, 6).value) + str(i), (sht0.range(i, 3).value, sht0.range(i, 5).value))#dict由3,4列换成了3,5列
    try:
        dicFCD.pop(None)
    except:
        pass
    return dicFCD


def cal_Lapmaxb():
    #原来x[1]换成了下式计算值
    lpamax_list=list(x[0]+10*math.log10(x[1]/20) for x in dicFCDvalues if (x[1] and x[0]))
    sum10nlist = list(math.pow(10, (x / 10)) for x in lpamax_list)  # 10的n次方列表
    sum10n = math.fsum(sum10nlist)  # 10的n次方列表求和
    # print('0的n次方列表求和:',sum10n)
    one_N = 1 / len(sum10nlist)  # 1/N
    # print('N:',len(sum10nlist))
    result = 10 * math.log10(one_N * sum10n)  # 结果
    return result

def getdianwei():
    dianwei = filexlsx[0:2]
    if '#' not in dianwei:
        dianwei += '#'
    return dianwei


for root, _, files in os.walk(r'C:\Users\Administrator\Desktop\噪声桌面\待计算'):
    for filexlsx in files:
        if 'xlsx' in filexlsx and ('~$' not in filexlsx):
            file24 = app2.books.open(os.path.join(root, filexlsx))
            sht0 = file24.sheets[0]
            if '23:00' not in str(sht0.range('a1793').value):
                print(filexlsx, '文件不是1823行')
            dicFCD = gendic()
            dicFCDvalues = list(dicFCD.values())  # 字典value
            try:
                lapmaxb_noround = cal_Lapmaxb()
                lapmaxb = round(lapmaxb_noround, 1)
            except Exception as e:
                print(1, filexlsx)
                print(e)
                file24.close()
                continue
            dianwei = getdianwei()
            list_result0 = [dianwei, sht0.range('a4').value,lapmaxb,lapmaxb+13]
            shtres.range('a{}'.format(result_flag)).value = list_result0
            file_result.save()
            file24.close()
            os.remove(os.path.join(root, filexlsx))
            result_flag += 1
app2.quit()
