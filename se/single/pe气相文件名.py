# -*- coding: utf-8 -*-
# date: 2022/7/18
import csv
import os

with open('1.csv', 'w', newline='') as f:
    csvw = csv.writer(f)
    dir1 = os.listdir()
    csvw.writerows([(i.replace('.raw', ''), os.path.join(os.getcwd(), i)) for i in dir1 if i.endswith('.raw')])
