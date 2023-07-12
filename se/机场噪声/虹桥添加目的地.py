import xlwings
import os

app_24 = xlwings.App(visible=True, add_book=False)
app_hbb = xlwings.App(visible=True, add_book=False)
file_hbb = app_hbb.books.open(r"C:\Users\Administrator\Desktop\噪声桌面\03.01虹桥加目的地\航班表.xlsx")
for root, _, files in os.walk(r'C:\Users\Administrator\Desktop\噪声桌面\03.01虹桥加目的地\03.03'):
    for filexlsx in files:
        if filexlsx == '航班表.xlsx':
            continue
        if 'xlsx' in filexlsx and ('~$' not in filexlsx):
            file24path = os.path.join(root, filexlsx)
            file24 = app_24.books.open(file24path)  # 24小时文件
            shtcount = file24.sheets.count  # sheet数量
            for sc in range(shtcount):
                sht = file24.sheets[sc]  # sht：其中一天的sheet
                sht_hb = file_hbb.sheets[sht.name]
                flag = 1
                for i in range(2, 600):
                    hbh_24 = sht.range('m{}'.format(i)).value
                    if hbh_24 is None:
                        continue
                    for j in range(flag + 1, 800):
                        hbh_hbb = sht_hb.range('b{}'.format(j)).value
                        if hbh_hbb == hbh_24:
                            flag = j
                            break
                    sht.range('r{}'.format(i)).value = sht_hb.range('d{}'.format(flag)).value
            file24.save()
            file24.close()
app_24.quit()
app_hbb.quit()