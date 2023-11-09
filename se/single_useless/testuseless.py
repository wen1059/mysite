# import numpy as np
# import pandas as pd
#
# df = pd.read_excel(r"\\10.1.78.254\环装-实验室\实验室共享\2023鸡场\闻亮2#\2#1001.xlsx", header=5)
# df = df.dropna(subset=['机型'], how='all')
# df = df[df['startTime'].isin(['startTime']) == False]
# print(df[df['备注'].notna()])
# te = df['航班号']
# print(te)
# idx0 = df.iloc[[0,2,4]]
# print(idx0)
import os
import shutil
path = r"C:\Users\Administrator\Desktop\学校相关\英语阅读纸"
os.chdir(path)
shutil.make_archive(r'..\123','zip')