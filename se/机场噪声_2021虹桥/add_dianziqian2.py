import glob
import os

import xlwings as xw

app = xw.App(visible=False, add_book=False)
path = os.getcwd()
for xlxfile in glob.glob(f'{path}/*.xlsx'):
    wb = app.books.open(xlxfile)
    sht = wb.sheets[0]
    sht.api.PageSetup.LeftFooter = "&G"
    sht.api.PageSetup.LeftFooterPicture.Filename = os.path.join(path, 'test.png')
    sht.api.PageSetup.LeftFooterPicture.Height = 31.5
    sht.api.PageSetup.LeftFooterPicture.Width = 391.5
    sht.api.PageSetup.CenterFooter = ""
    sht.api.PageSetup.RightFooter = "" + chr(10) + "第&P页,共&N页&9" + chr(10) + " 2021年3月29日启用"
    wb.save()
app.quit()
