import os
import xlwings

app_24 = xlwings.App(visible=False, add_book=False)
walkpath = os.getcwd()
for root, _, files in os.walk(walkpath):
    for filexlsx in files:
        if filexlsx[-5:-1] != '.xls' or '~$' in filexlsx:
            continue
        file24path = os.path.join(root, filexlsx)
        file24 = app_24.books.open(file24path)  # 24小时文件
        sht = file24.sheets[0]
        for i in range(1, 2080):
            if sht.range('a{}'.format(i)).value == '机场噪声数据分析记录（I）':
                sht.range('a{}'.format(i)).value = '机场周围飞机噪声数据分析记录（I）'
            elif sht.range('a{}'.format(i)).value == '机场噪声数据分析记录（II）':
                sht.range('a{}'.format(i)).value = '机场周围飞机噪声数据分析记录（II）'
        file24.save()
        file24.close()
        print(f'{filexlsx} 已完成')
app_24.kill()
print('\n全部完成')
input()
