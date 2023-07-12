import os
import xlwings
import csv


def yieldsht(walkpath):
    """
    生成每个要处理的表
    :return:
    """
    app_24 = xlwings.App(visible=False, add_book=False)  # 待计算文件
    for root, _, files in os.walk(walkpath):
        for filexlsx in files:
            if filexlsx[-5:-1] != '.xls' or '~$' in filexlsx:
                continue
            file24path = os.path.join(root, filexlsx)
            file24 = app_24.books.open(file24path)  # 24小时文件
            yield file24.name, file24.sheets[0]
            file24.close()
    app_24.quit()


def count(name, sht):
    def gdic():
        dic = {}
        dic.setdefault('east', {})
        dic.setdefault('west', {})
        for i in dic:
            dic[i].setdefault('qifei', {})
            for j in dic[i]:
                dic[i][j].setdefault('south', 0)
                dic[i][j].setdefault('north', 0)
            dic[i].setdefault('jiangluo', {})
            for j in dic[i]:
                dic[i][j].setdefault('south', 0)
                dic[i][j].setdefault('north', 0)
        # print(dic)
        return dic

    # dic = gdic()
    dic = {'east': {'qifei': {'south': 0, 'north': 0}, 'jiangluo': {'south': 0, 'north': 0}},
           'west': {'qifei': {'south': 0, 'north': 0}, 'jiangluo': {'south': 0, 'north': 0}},
           'east2': {'qifei': {'south': 0, 'north': 0}, 'jiangluo': {'south': 0, 'north': 0}},
           'west2': {'qifei': {'south': 0, 'north': 0}, 'jiangluo': {'south': 0, 'north': 0}}
           }
    # print(dic)
    for i in range(1, 1000):
        paodao = sht.range(f'f{i}').value
        # print(paodao)
        qijiang = sht.range(f'd{i}').value
        fangxaing = sht.range(f'e{i}').value
        if paodao in ['17R', '35L']:  # 东跑道
            if qijiang == '起飞':
                if '向南' in fangxaing:
                    dic['east']['qifei']['south'] += 1
                elif '向北' in fangxaing:
                    dic['east']['qifei']['north'] += 1
            elif qijiang == '降落':
                if '向南' in fangxaing:
                    dic['east']['jiangluo']['south'] += 1
                    # print(i)
                elif '向北' in fangxaing:
                    dic['east']['jiangluo']['north'] += 1
        elif paodao in ['17L', '35R']:  # 西跑道
            if qijiang == '起飞':
                if '向南' in fangxaing:
                    dic['west']['qifei']['south'] += 1
                elif '向北' in fangxaing:
                    dic['west']['qifei']['north'] += 1
            elif qijiang == '降落':
                if '向南' in fangxaing:
                    dic['west']['jiangluo']['south'] += 1
                elif '向北' in fangxaing:
                    dic['west']['jiangluo']['north'] += 1
        elif paodao in ['16R', '34L']:  # 东跑道
            if qijiang == '起飞':
                if '向南' in fangxaing:
                    dic['east2']['qifei']['south'] += 1
                elif '向北' in fangxaing:
                    dic['east2']['qifei']['north'] += 1
            elif qijiang == '降落':
                if '向南' in fangxaing:
                    dic['east2']['jiangluo']['south'] += 1
                elif '向北' in fangxaing:
                    dic['east2']['jiangluo']['north'] += 1
        elif paodao in ['16L', '34R']:  # 西跑道
            if qijiang == '起飞':
                if '向南' in fangxaing:
                    dic['west2']['qifei']['south'] += 1
                elif '向北' in fangxaing:
                    dic['west2']['qifei']['north'] += 1
            elif qijiang == '降落':
                if '向南' in fangxaing:
                    dic['west2']['jiangluo']['south'] += 1
                    # print(i)
                elif '向北' in fangxaing:
                    dic['west2']['jiangluo']['north'] += 1
    result = (dic['east']['qifei']['south'],
              dic['east']['qifei']['north'],
              dic['east']['jiangluo']['south'],
              dic['east']['jiangluo']['north'],
              dic['west']['qifei']['south'],
              dic['west']['qifei']['north'],
              dic['west']['jiangluo']['south'],
              dic['west']['jiangluo']['north'],
              dic['east2']['qifei']['south'],
              dic['east2']['qifei']['north'],
              dic['east2']['jiangluo']['south'],
              dic['east2']['jiangluo']['north'],
              dic['west2']['qifei']['south'],
              dic['west2']['qifei']['north'],
              dic['west2']['jiangluo']['south'],
              dic['west2']['jiangluo']['north']
              )
    return result


with open(r"C:\Users\Administrator\Desktop\新建文件夹 (2)\1.csv", 'w', newline='') as f:
    csv_f = csv.writer(f)
    for name, sht in yieldsht(r"C:\Users\Administrator\Desktop\新建文件夹 (2)"):
        result = ((name,) + count(name, sht))
        csv_f.writerow(result)
