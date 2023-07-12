import xlwings, os

app = xlwings.App(visible=True, add_book=False)
for root, _, files in os.walk(r'C:\气象'):
    for filexlsx in files:
        file = app.books.open(os.path.join(root, filexlsx))
        lenshtorg = len(file.sheets)
        shtres = file.sheets.add(after=file.sheets[-1])
        l_fengsu_min = []
        l_fengsu_max = []
        l_shidu_min = []
        l_shidu_max = []
        for i in range(lenshtorg):
            if 'Sheet' in file.sheets[i].name:
                continue
            l_fengsu_min.extend(file.sheets[i].range('h3').expand('down').value)
            l_fengsu_max.extend(file.sheets[i].range('i3').expand('down').value)
            l_shidu_min.extend(file.sheets[i].range('l3').expand('down').value)
            l_shidu_max.extend(file.sheets[i].range('m3').expand('down').value)
        l_fengsu_min.sort()
        l_fengsu_max.sort()
        l_shidu_min.sort()
        l_shidu_max.sort()
        shtres.range('a1').value = ['风速min', '风速max', '湿度min', '湿度max']
        shtres.range('a2').value = [l_fengsu_min[0], l_fengsu_max[-1], l_shidu_min[0], l_shidu_max[-1]]
        file.save()
        file.close()
app.quit()
