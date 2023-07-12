import os
from itertools import islice
import csv


def yieldawa(walkpath):
    for root, _, files in os.walk(walkpath):
        for file in files:
            if '.awa' in file.lower():
                yield root, file


def change(awa_org, awa):
    """
    按顺序修改awa事件编号
    """
    with open(awa_org, 'r') as f_org, open(awa, 'w', newline='') as f_new:
        reader = csv.reader(f_org, delimiter='\t')
        writer = csv.writer(f_new, delimiter='\t')
        for line in islice(reader, 0, 6):
            writer.writerow(line)
        i = 1
        for line in islice(reader, 0, None):
            if line:
                if line[0][0] == ' ':
                    line[0] = ' ' * (8 - len(str(i))) + str(i)
                    i += 1
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
