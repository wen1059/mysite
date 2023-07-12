# -*- coding: utf-8 -*-
# date: 2022-11-24
import time
import random

# 输入自定义时间,生成格式为struct_time
a = time.strptime('2022-09-05 09:05:22', '%Y-%m-%d %H:%M:%S')
# 将struct_time格式时间转换为时间戳
b = time.mktime(a)
# 时间戳转换为struct_time格式
a_ = time.localtime(b)
# 将struct_time时间格式化为指定形式的字符串
'''
变量	含义
%a	本地化的缩写星期中每日的名称。
%A	本地化的星期中每日的完整名称。
%b	本地化的月缩写名称。
%B	本地化的月完整名称。
%c	本地化的适当日期和时间表示。
%d	十进制数 [01,31] 表示的月中日。
%H	十进制数 [00,23] 表示的小时（24小时制）。
%I	十进制数 [01,12] 表示的小时（12小时制）。
%j	十进制数 [001,366] 表示的年中日。
%m	十进制数 [01,12] 表示的月。
%M	十进制数 [00,59] 表示的分钟。
%p	本地化的 AM 或 PM 。
%S	十进制数 [00,61] 表示的秒。
%U	十进制数 [00,53] 表示的一年中的周数（星期日作为一周的第一天）。 在第一个星期日之前的新年中的所有日子都被认为是在第 0 周。
%w	十进制数 [0(星期日),6] 表示的周中日。
%W	十进制数 [00,53] 表示的一年中的周数（星期一作为一周的第一天）。 在第一个星期一之前的新年中的所有日子被认为是在第 0 周。
%x	本地化的适当日期表示。
%X	本地化的适当时间表示。
%y	十进制数 [00,99] 表示的没有世纪的年份。
%Y	十进制数表示的带世纪的年份。
%z	时区偏移以格式 +HHMM 或 -HHMM 形式的 UTC/GMT 的正或负时差指示，其中H表示十进制小时数字，M表示小数分钟数字 [-23:59, +23:59] 。
%Z	时区名称（如果不存在时区，则不包含字符）。
%%	字面的'%' 字符。'''
c = time.strftime('%Y-%m-%d %H:%M:%S', a)


def gentime():
    start_struck = time.strptime('2022-12-02 09:05:22', '%Y-%m-%d %H:%M:%S')
    start = time.mktime(start_struck)
    while True:
        nexttime_strucf = time.strftime('%y-%m-%d %H:%M:%S', time.localtime(start))
        yield nexttime_strucf
        start += random.randint(60 * 9, 60 * 13)


g = gentime()
a, b = next(g), next(g)
for _ in range(100):
    # dosomething
    print(a, b)
    a, b = b, next(g)
