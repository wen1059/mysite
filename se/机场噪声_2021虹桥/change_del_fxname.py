import os
import re
# import ctypes
#
# kernel32 = ctypes.windll.kernel32
# kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)

cfname = []
regx = re.compile(r'\d{2}#\d{4}')
# walkpath = os.getcwd()
walkpath=r"C:\Users\Administrator\Desktop\虹桥噪声桌面\浦东优先分析点位\output"
for root, _, files in os.walk(walkpath):
    for filexlsx in files:
        if filexlsx[-5:-1] != '.xls' or '~$' in filexlsx:
            continue
        oldname = filexlsx
        oldnamepath = os.path.join(root, oldname)
        try:
            newname = regx.search(filexlsx).group(0) + '.xlsx'
        except:
            continue
        # newname2 = regx.search(filexlsx).group(0) + '_2.xlsx'
        newnamepath = os.path.join(root, newname)
        # newnamepath2 = os.path.join(root, newname2)
        try:
            os.rename(oldnamepath, newnamepath)
            print(f'{oldname} --> {newname}')
        except Exception as e:
            cfname.append(oldnamepath)
if cfname:
    print('以下文件重名，所以未修改')
    for i in cfname:
        print(i)
print('\n全部完成\n')
# input()
