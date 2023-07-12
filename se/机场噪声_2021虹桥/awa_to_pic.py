import csv
from itertools import islice
from matplotlib import pyplot as plt
import os
from concurrent.futures import ProcessPoolExecutor
import time


def draw(awapath):
    lst = []
    with open(awapath) as f:
        reader = csv.reader(f, delimiter='\t')
        for line in islice(reader, 6, None):
            if not line:
                break
            try:
                lst.append(float(line[3].replace(' ', '')))
            except:
                lst.append(0)
    # fig = plt.figure(figsize=(15, 8))
    plt.ylim(min(lst)-10, max(lst))
    plt.bar(range(len(lst)), lst, width=1)
    plt.savefig(awapath.replace('.AWA', '.png'), dpi=600)
    # print(savepath)
    plt.clf()


def yieldawa(path):
    for root, _, files in os.walk(path):
        for awa in files:
            if '.AWA' not in awa.upper():
                continue
            awapath = os.path.join(root, awa)
            if os.path.exists(awapath.replace('.AWA', '.png')):
                continue
            yield awapath


if __name__ == '__main__':
    with ProcessPoolExecutor() as pool:
        [pool.submit(draw, awa) for awa in yieldawa(r"C:\Users\Administrator\Desktop\新建文件夹")]