import xlwings

app = xlwings.App(visible=True, add_book=False)
file = app.books.open(r'C:\Users\Administrator\Desktop\噪声桌面\计算结果\12个点机型比例前后统计 20210208.xlsx')
sht_org = file.sheets[0]
sht_tab = file.sheets.add(after=file.sheets[-1])
jx_list = ['738.0', '320.0', '321.0', '333.0', '7M8', '773.0', '73G', '332.0', '789.0', '788.0']
sht_tab.range('b1').value = jx_list + ['other']


def gendict(sht):
    '''
    生成二级嵌套字典 {日期：{机型：数量，}，}
    :param sht: 按点位统计的表
    :return:dic
    '''
    dic = {}
    for i in range(3, 6300):
        date = sht.range('b{}'.format(i)).value
        # print(sht.range('a{}'.format(i)).value,date)
        if date is None:
            continue
        jx = sht.range('c{}'.format(i)).value
        count = sht.range('e{}'.format(i)).value
        # count = sht.range('g{}'.format(i)).value #剔除后架次
        if date not in dic:  # 如果日期不在字典
            dic.setdefault(date, {'other': 0})  # 添加此日期，并且初始化“其他机型”为0
        if jx not in dic[date]:  # 如果这一天这个机型不在字典
            if str(jx) in jx_list:  # 如果是识别的机型
                dic[date].setdefault(jx, count)  # 添加机型和次数到字典
            else:
                dic[date]['other'] += count  # 否则数量加到其他机型
        else:  # 如果这一天这个机型在字典
            dic[date][jx] += count  # 增加机型数量
    return dic


dic = gendict(sht_org)
# print(dic)
sht_tab.range('a2').options(transpose=True).value = list(dic.keys())  # 所有统计在字典的日期放在a2开始的第一列
rows = len(dic) + 1  # 表格行数
cols = 12  # 表格列数
for i in range(1, rows):
    for j in range(1, cols):
        key_date = sht_tab[i, 0].value
        # print(key_date)
        key_jx = sht_tab[0, j].value
        # print(key_jx)
        try:
            sht_tab[i, j].value = dic[key_date][key_jx]
        except:
            sht_tab[i, j].value = 0
        # print('value',dic[key_date][key_jx])
