import xlwings


file = xlwings.books.active
sht = file.sheets[0]
sht.api.Range("A1").AutoFilter(Field=1)
oss = sht.range('a1').expand('down').value  # 所有样品编号带重复
os = list(set(oss))  # 所有样品编号不重复
oindexs = [oss.index(o) + 1 for o in os]  # 每个样品编号所在的行号,索引对应到excel要+1
oindexs.sort()
colorflag = True  # true为填充底色
for pre, next_ in zip(oindexs, oindexs[1:] + [len(oss) + 1]):  # pre,next为上一个编号和下一个编号所在的行
    if colorflag:
        sht.range(f'a{pre}:d{next_ - 1}').color = 226, 239, 218
    colorflag = False if colorflag else True  # 切换colorflag状态，达到间隔填充效果