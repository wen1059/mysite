import os
import xlwings

app_24 = xlwings.App(visible=False, add_book=False)
for root, _, files in os.walk(os.getcwd()):
    for filexlsx in files:
        if filexlsx[-5:-1] != '.xls' or '~$' in filexlsx:
            continue
        file24path = os.path.join(root, filexlsx)
        file24 = app_24.books.open(file24path)  # 24小时文件
        sht=file24.sheets[0]
        for i in range(3, 2080):
            if lepn:=sht.range('d{}'.format(i)).value==0:
                print(filexlsx,f'第{i}行','lepn 0')
                continue
            if te := sht.range('d{}'.format(i)).value == 0:
                print(filexlsx, f'第{i}行', 'TE 0')
        file24.close()
app_24.kill()
print('完成')
input()