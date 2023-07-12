# -*- coding: utf-8 -*-
# date: 2022/7/7
import xlwings

file = xlwings.books.active
shtnames = [i.name for i in file.sheets]
shtnames.sort(key=None)  # 可以用lamda函数按规则排序
for index, name in enumerate(shtnames):
    file.sheets[name].api.Move(After=file.sheets[shtnames[index - 1]].api)
# for i in range(1, len(shtnames)):
#     # .api后面的函数以及参数首字母需大写
#     file.sheets[shtnames[i]].api.Move(After=file.sheets[shtnames[i - 1]].api)

# 或者以下方式
# for name in shtnames:
#     # sheets.copy(before=***)等价于sheets.api.Copy(Before=***)
#     file.sheets[name].copy()
#     file.sheets[name].delete()
#     file.sheets[-1].name = name
