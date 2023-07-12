"""
调整因excel修改导致的格式错位
"""
import csv
from itertools import islice
import os


def yieldawa(walkpath):
    for root, _, files in os.walk(walkpath):
        for file in files:
            if '.awa' in file.lower():
                yield root, file


def change(awa_org, awa):
    """
    按顺序修改awa事件编号
    """
    with open(awa_org, 'r') as f_org, \
            open(awa, 'w', newline='') as f_new:
        reader = csv.reader(f_org, delimiter='\t')
        writer = csv.writer(f_new, delimiter='\t')
        for line in islice(reader, 0, 6):
            writer.writerow(line)
        for line in islice(reader, 0, None):
            # print(line)
            line[0] = ' ' * (8 - len(line[0])) + line[0]
            if len(line[1]) in [1, 2]:
                line[1] += '.0'
            line[1] = ' ' * 4 + line[1] + ' '
            for i in range(2, len(line)):
                line[i] = line[i].replace('-', '')
                if len(line[i]) in [1, 2]:
                    line[i] += '.0'
                line[i] = ' ' * (5 - len(line[i])) + line[i] + ' '
            writer.writerow(line)


def tongbutime(orgfile, newfile):
    atime = os.path.getatime(orgfile)
    mtime = os.path.getmtime(orgfile)
    os.utime(newfile, (atime, mtime))


def run(walkpath):
    for root, file in yieldawa(walkpath):
        awa = os.path.join(root, file)
        awa_org = os.path.join(root, file.replace('.', '_org.'))
        os.rename(awa, awa_org)
        change(awa_org, awa)
        tongbutime(awa_org, awa)


run(r"C:\Users\Administrator\Desktop\新建文件夹")
