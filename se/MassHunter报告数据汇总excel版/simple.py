import xlwings
file=xlwings.books.active
file.sheets.add(name='last',after='DESIGN-SAMP')
lastsht=file.sheets('last')
lastsht[1,0].options(transpose=True).value=file.sheets[1].range('a16').expand('down').value
for i in range(1,file.sheets.count-2):
    lastsht[0,i].value=file.sheets[i].name
    lastsht[1,i].options(transpose=True).value=file.sheets[1].range('f16').expand('down').value
rows=lastsht.range('a2').expand('down').rows.count
for i in range(rows).__reversed__():
    if lastsht[i,0].value in ['Compound','4-溴氟苯（surr）','二溴氟甲烷（surr）','甲苯-d8（surr）']:
        lastsht.api.rows(i+1).delete
