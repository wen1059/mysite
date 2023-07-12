import os
import xlwings

def yieldsht(walkpath):
    """
    生成每个要处理的表
    :return:
    """
    app_24 = xlwings.App(visible=False, add_book=False)  # 待计算文件
    for root, _, files in os.walk(walkpath):
        for filexlsx in files:
            if filexlsx[-5:-1] != '.xls' or '~$' in filexlsx:
                continue
            file24path = os.path.join(root, filexlsx)
            file24 = app_24.books.open(file24path)  # 24小时文件
            yield file24.name, file24.sheets[0]
            file24.close()
    app_24.kill()

err=[]
for filenane,sht in yieldsht(r"C:\Users\Administrator\Desktop\虹桥噪声桌面\最终版5.9"):
    print(filenane)
    for i in range(3, 2080):
        jx = sht.range('j{}'.format(i)).value
        if jx==' ':
            err.append((filenane,i))
print(err)
for i in err:
    print(i)