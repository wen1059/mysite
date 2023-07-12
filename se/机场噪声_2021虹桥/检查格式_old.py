"""
检查格式：行数，背景干扰的多缺
"""
import xlwings, os

app = xlwings.App(visible=True, add_book=False)

for root, _, files in os.walk(r'C:\Users\Administrator\Desktop\噪声桌面\待计算'):
    for filexlsx in files:
        if 'xlsx' in filexlsx and ('~$' not in filexlsx):
            file24 = app.books.open(os.path.join(root, filexlsx))
            sht0 = file24.sheets[0]
            for i in range(1, 1648):
                if sht0.range(f'a{i}').value != '谱图：':  # 检查行数
                    print(filexlsx, '行数不对')
                eval = sht0.range('e{}'.format(i)).value
                gval = sht0.range('g{}'.format(i)).value
                lval = sht0.range('l{}'.format(i)).value
                # print(eval,fval,kval)
                if lval == '航班重合':  # 检查航班重合
                    print(filexlsx, '[' + str(i) + ']', '航班重合')
                if eval == None and (gval not in [None, '机型']):  # 事件空，航班有
                    if lval == None:  # 备注没有的话缺了
                        print(filexlsx, '[' + str(i) + ']', '缺')
                if eval != None and gval != None:  # 事件和航班都有
                    if lval not in [None, '备注']:  # 备注有的话多了
                        print(filexlsx, '[' + str(i) + ']', '多')
            file24.close()
            try:
                os.remove(os.path.join(root, filexlsx))
            except:
                pass
app.quit()
