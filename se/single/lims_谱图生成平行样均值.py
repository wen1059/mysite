import traceback
import xlwings
try:
    file = xlwings.books.active
    # sheet:xlwings.main.Sheet
    for sheet in file.sheets:
        # sheetname改大写
        sheet.name = sheet.name[0:-2].upper()
        # datafile单元格改大写
        sheet.range('d7').value = str(sheet.range('d7').value).upper()
    # shtsnames_px = [i.name[:9] for i in file.sheets if '-PX-01' in i.name.upper()]
    # for shtname in shtsnames_px:
    #     px1 = file.sheets[shtname + '-PX-01']
    #     # 如果其中一个平行样写成了原编号，把他改为加上-px-02
    #     if shtname + '-PX-02' not in [sht.name for sht in file.sheets]:
    #         file.sheets[shtname].range('d7').value = file.sheets[shtname].range('d7').value.replace('.D', '-px-02.D')
    #         file.sheets[shtname].name = shtname + '-PX-02'
    #     px2 = file.sheets[shtname + '-PX-02']
    #     file.sheets.add(name=shtname, after=file.sheets[-1])
    #     px = file.sheets[shtname]
    #     px.range('a1').value = px1.range('a1:h150').value
    #     fpx1 = px1.range('f1:f150').options(transpose=True).value
    #     fpx2 = px2.range('f1:f150').options(transpose=True).value
    #     px.range('f1:f150').options(transpose=True).value = [
    #         (i + j) / 2 if (isinstance(i, float) and isinstance(j, float)) else i for i, j in zip(fpx1, fpx2)]
except Exception:
    traceback.print_exc()
    input()
