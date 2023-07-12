# import os
import xlwings


def trans(jd):
    result = None
    if not str(jd).isdigit():
        return
    if 348.76 <= jd <= 360 or 0 <= jd <= 11.25:
        result = ('北', 'N')
    elif 11.26 <= jd <= 33.75:
        result = ('北东北', 'NNE')
    elif 33.76 <= jd <= 56.25:
        result = ('东北', 'NE')
    elif 56.26 <= jd <= 78.75:
        result = ('东东北', 'ENE')
    elif 78.86 <= jd <= 101.25:
        result = ('东', 'E')
    elif 101.26 <= jd <= 123.75:
        result = ('东东南', 'ESE')
    elif 123.76 <= jd <= 146.25:
        result = ('东南', 'SE')
    elif 146.26 <= jd <= 168.75:
        result = ('南东南', 'SSE')
    elif 168.76 <= jd <= 191.25:
        result = ('南', 'S')
    elif 191.26 <= jd <= 213.75:
        result = ('南西南', 'SSW')
    elif 213.76 <= jd <= 236.25:
        result = ('西南', 'SW')
    elif 236.26 <= jd <= 258.75:
        result = ('西西南', 'WSW')
    elif 258.76 <= jd <= 281.25:
        result = ('西', 'W')
    elif 281.26 <= jd <= 303.75:
        result = ('西西北', 'WNW')
    elif 303.76 <= jd <= 326.25:
        result = ('西北', 'NW')
    elif 326.26 <= jd <= 348.75:
        result = ('北西北', 'NNW')
    return result


for sht in xlwings.books.active.sheets:
    yd=sht.range('j1:q25').value
    sht.range('k1').value=yd
    sht.range('j1').value=None
    for row in range(2, 26):
        jd1 = sht.range(f'g{row}').value
        result1 = trans(jd1)
        sht.range(f'i{row}').value=result1
        jd2 = sht.range(f'q{row}').value
        result2 = trans(jd2)
        sht.range(f's{row}').value=result2
