import xlwings
import os
import time
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)
print('请把此程序放在待汇总excel报告的同级或上级目录,可同时汇总多个文件\n结果会保存在“汇总结果.xlsx”\n请确保已安装Microsoft Excel\n')
app_result = xlwings.App(visible=True, add_book=False)
calrootpath = os.getcwd()
if not os.path.exists('汇总结果.xlsx'):
    file_result = app_result.books.add()
    file_result.save('汇总结果.xlsx')
else:
    file_result = app_result.books.open(r'汇总结果.xlsx')
shtres = file_result.sheets.add(after=file_result.sheets[-1],
                                name=time.strftime('%m%d.%H%M%S', time.localtime(time.time())))

app_cal = xlwings.App(visible=False, add_book=False)
flag = 1
for root, _, files in os.walk(calrootpath):
    for filexlsx in files:
        if filexlsx == '汇总结果.xlsx':
            continue
        if '.xlsx' in filexlsx and ('~$' not in filexlsx):
            file = app_cal.books.open(os.path.join(root, filexlsx))
            shtcount = file.sheets.count
            if flag == 1:
                shtres[1, 0].options(transpose=True).value = file.sheets[1].range('a13', 'a150').value
            for sc in range(1, shtcount - 1):
                sht = file.sheets[sc]
                shtres[0, flag].value = sht.name
                print(sht.name, '完成')
                shtres[1, flag].options(transpose=True).value = sht.range('g13', 'g150').value
                flag += 1
            file.close()
app_cal.quit()
for i in range(1, 150).__reversed__():
    if shtres[i, 0].value in ['Compound', '4-溴氟苯（surr）', '二溴氟甲烷（surr）', '甲苯-d8（surr）', None, 'Compound Graphics']:
        shtres[i, 0].api.EntireRow.Delete()
file_result.save()
print('汇总完成', '按任意键关闭')
input()
