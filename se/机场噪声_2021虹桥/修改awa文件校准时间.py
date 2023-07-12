"""
修改awa文件第三行校准时间
例子：Calibrate@2020-09-30 12:15:48 Lx=-28.7dB
"""
import csv
import re
import os


def yieldawa(walkpath):
    for root, _, files in os.walk(walkpath):
        for file in files:
            if '.awa' in file.lower():
                yield root, file


def readtime(file):
    """
    读取要修改成的新时间，从csv到dic
    :return:
    """
    d = {}
    with open(file) as f:
        lines = csv.reader(f)
        for line in lines:
            d.setdefault(line[0], line[1])
    return d


def change(awa_org, awa, newtime):
    """
    修改awa校准时间
    :param awa_org:源文件
    :param awa: 新文件
    :param newtime: 修改的新时间
    :return:
    """
    regx = re.compile(r'(?<=Calibrate@).+(?= Lx=)')
    with open(awa_org, 'r') as f_org, \
            open(awa, 'w', newline='') as f_new:
        txt_org = f_org.read()
        txt_new = regx.sub(newtime, txt_org)
        f_new.write(txt_new)
        print(os.path.basename(awa), newtime)


def tongbutime(orgfile, newfile):
    atime = os.path.getatime(orgfile)
    mtime = os.path.getmtime(orgfile)
    os.utime(newfile, (atime, mtime))


# awa的根目录
walkpath = r'C:\Users\Administrator\Desktop\新建文件夹 (2)'
# 时间的csv路径
newtimes = readtime(r"C:\Users\Administrator\Desktop\新建文件夹 (2)\1.csv")
for root, file in yieldawa(walkpath):
    awa = os.path.join(root, file)
    awa_org = os.path.join(root, file.replace('.', '_org.'))
    os.rename(awa, awa_org)
    dianwei = re.search(r'\d{1,2}#',file)
    newtime = newtimes[dianwei]
    # 不需要替换的在csv里面填上0
    if newtime == 0:
        continue
    change(awa_org, awa, newtime)
    tongbutime(awa_org, awa)
    os.remove(awa_org)
