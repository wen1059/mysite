import PyPDF2
import os
import re
import xlwings

app1 = xlwings.App(visible=True, add_book=False)  # 结果excel文件
if not os.path.exists('计算结果.xlsx'):
    file_result = app1.books.add()
    file_result.save('计算结果.xlsx')
else:
    file_result = app1.books.open(r'计算结果.xlsx')
shtres = file_result.sheets.add(after=file_result.sheets[-1])
row = 1
for root, _, files in os.walk(os.getcwd()):
# for root, _, files in os.walk(r"C:\Users\Administrator\Desktop\新建文件夹 (2)"):
    for filexlsx in files:
        if '.pdf' in filexlsx:
            filepath = os.path.join(root, filexlsx)
            fileobj = open(filepath, 'rb')
            reader = PyPDF2.PdfFileReader(fileobj)
            resultstr = ''
            for i in range(reader.numPages):
                resultstr += reader.getPage(i).extractText()
            print(resultstr)
            regx_name = re.compile(r'.+\\(.+?\.D)')
            dataname = regx_name.search(resultstr).group(1)
            # print(name)
            regx_pcb = re.compile(r' (.+?) {4}(PCB\d{2,3})')
            pcb = regx_pcb.findall(resultstr)
            print(pcb)
            for value, pcbname in pcb:
                value = value.split()[-1]
                shtres.range('a{}'.format(row)).value = dataname
                shtres.range('b{}'.format(row)).value = pcbname
                shtres.range('c{}'.format(row)).value = value
                row += 1
        row += 1
