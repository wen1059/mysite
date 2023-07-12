"""
修改awa文件第三行校准时间
例子：Calibrate@2020-09-30 12:15:48 Lx=-28.7dB
文件不含1#这样的编号，靠文件夹的点位名称识别
2021.11.17更新 进一步修改仪器编号和db值
"""
import csv
import re
import os
from concurrent.futures import ProcessPoolExecutor


def yieldawa(walkpath):
    for root, _, files in os.walk(walkpath):
        for file in files:
            if '.awa' in file.lower():
                yield root, file


def readtime(file):
    """
    读取要修改成的新时间，从csv到dic
    line[0]是点位中文名称
    :return:
    """
    d = {}
    with open(file) as f:
        lines = csv.reader(f)
        for line in lines:
            d.setdefault(line[0], (line[1], line[2], line[3]))
    return d


def change(awa_org, awa, newtime):
    """
    修改awa校准时间
    :param awa_org:源文件
    :param awa: 新文件
    :param newtime: 修改的新时间
    :return:
    """
    regx_tm = re.compile(r'(?<=Calibrate@).+(?= Lx=)')
    regx_yq = re.compile(r'(?<=Serial:)\d+')
    regx_db = re.compile(r'(?<=Lx=).+(?=dB)')
    with open(awa_org, 'r', errors='ignore') as f_org, \
            open(awa, 'w') as f_new:
        txt_org = f_org.read()
        txt_tmp1 = regx_tm.sub(newtime[0], txt_org)
        txt_tmp2 = regx_yq.sub(newtime[1], txt_tmp1)
        txt_new = regx_db.sub(newtime[2], txt_tmp2)
        f_new.write(txt_new)
        # print(awa, newtime)


def tongbutime(orgfile, newfile):
    atime = os.path.getatime(orgfile)
    mtime = os.path.getmtime(orgfile)
    os.utime(newfile, (atime, mtime))


def run(root, file, newtimes):
    dianwei = re.search(r"A\d{8} (.+)\\\d{4}", root).group(1)
    newtime = newtimes[dianwei]
    # 不需要替换的在csv里面填上0
    # if newtime == '0':
    #     return
    awa = os.path.join(root, file)
    awa_org = os.path.join(root, file.replace('.', '_org.'))
    os.rename(awa, awa_org)
    change(awa_org, awa, newtime)
    tongbutime(awa_org, awa)
    os.remove(awa_org)


if __name__ == '__main__':
    newtimes = readtime(r"C:\Users\Administrator\Desktop\新建文件夹 (2)\1.csv")
    with ProcessPoolExecutor() as pool:
        for root, file in yieldawa(r'C:\Users\Administrator\Desktop\新建文件夹 (2)'):
            pool.submit(run, root, file, newtimes)
