import numpy as np
import pandas as pd
df = pd.read_excel(r"\\10.1.78.254\环装-实验室\实验室共享\2024浦东机场数据比对\分析文件\建西#0829.xlsx",header=None)
df = df.replace(np.NAN,None)
print(df.head(10))
data = df.values.tolist()
print(type(data))
for line in data[:10]:
    print(line)
# import xlwings
# f = xlwings.books.open(r"\\10.1.78.254\环装-实验室\实验室共享\2024浦东机场数据比对\分析文件\建西#0829.xlsx")
# sht = f.sheets[0]
# values = sht.used_range.value
# for line in values[:10]:
#     print(line)