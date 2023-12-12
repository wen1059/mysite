import xlwings
import re

file = xlwings.books.active
for i in range(6):
    sht = file.sheets[i]
    for j in range(2, 1490):
        data = sht.range('e{}'.format(j)).value
        if not data:
            continue
        regx = re.compile(r'METAR ZS.. \d{6}Z (...)(..).*MPS')
        # print(regx.findall(transdata))

        fengxiang = regx.findall(data)[0][0]
        fx_result = ''
        try:
            fengxiang = int(fengxiang)
        except Exception as e:
            fx_result = 'VRB'
            print(e)
        else:
            if 0 <= fengxiang <= 90 or 270 <= fengxiang <= 360:
                fx_result = 'North'
            elif 90 < fengxiang < 270:
                fx_result = 'South'
        finally:
            sht.range('g{}'.format(i)).value = fx_result

        fengsu = int(regx.findall(data)[0][1])
        fs_result = 1 if fengsu > 5 else 0
        sht.range('h{}'.format(i)).value = fs_result

        rain_result = 1 if '-RA' in data else 0
        sht.range('i{}'.format(i)).value = rain_result
