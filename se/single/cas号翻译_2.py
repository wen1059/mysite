# -*- coding: utf-8 -*-
# date: 2022-10-26
"""
根据化合物名称或CAS号查找化合物信息（主要查CAS号和名称），chemicalbook查询。
"""
import requests
import csv
from lxml import etree


def searchinfo(compand: str):
    """
    根据化合物名称或CAS号查找化合物信息
    :param compand:化合物名称或CAS号
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    }
    htm = requests.get(f'https://www.chemicalbook.com/Search.aspx?keyword={compand}', headers=headers, timeout=5)
    tree = etree.HTML(htm.text)
    if compand.replace('-', '').isdigit():  # 输入的是CAS号
        name = tree.xpath('//*[@id="mbox"]/tr[3]/td[2]/a/text()')
        name = name[0] if name else None
        cas = compand
    else:  # 输入的是化合物名称
        name = compand
        cas = tree.xpath('//*[@id="mbox"]/tr[6]/td[2]/text()')
        cas = cas[0] if cas else None
    return [name, cas]


def writeinfo(csvpath):
    """
    读取csv中的化合物，翻译，再写入原csv
    :param csvpath:
    :return:
    """
    writecache = []
    with open(csvpath, 'r+', newline='') as f:
        reader = csv.reader(f)
        for line in reader:
            compand = line[0]
            info = searchinfo(compand)
            print([compand, info])
            writecache.append(info)
        f.seek(0)
        writer = csv.writer(f)
        writer.writerows(writecache)


def showinfo(compunds: str):
    """
    直接显示化合物cas号到控制台
    :param compunds:
    """
    compunds = compunds.split()
    for compund in compunds:
        info = searchinfo(compund)
        print(compund, info)


if __name__ == '__main__':
    # writecas(r"C:\Users\Administrator\Desktop\新建文件夹\工作簿1.csv")
    compunds = """
N-亚硝基二甲胺
苯胺
双（2-氯乙基）醚
双（2-氯异丙基）醚
N-亚硝基二丙胺
六氯乙烷
硝基苯
异佛尔酮
双（2-氯乙氧基）甲烷
2,4-二氯酚
萘
间硝基氯苯
对硝基氯苯
邻硝基氯苯
六氯环戊二烯
2,4,6-三氯酚
2-氯萘
对二硝基苯
邻苯二甲酸二甲酯
间二硝基苯
2,6-二硝基甲苯
邻二硝基苯
苊烯
苊
2,4-二硝基甲苯
2,4-二硝基氯苯
邻苯二甲酸二乙酯
4-氯二苯醚
芴
偶氮苯
2,4,6-三硝基甲苯
4-溴二苯醚
六氯苯
五氯酚
菲
蒽
咔唑
邻苯二甲酸二丁酯
荧蒽
芘
邻苯二甲酸丁苄酯
苯并[a]蒽
邻苯二甲酸二（2-乙基己）酯
䓛
邻苯二甲酸二辛酯
苯并[b]荧蒽
苯并[k]荧蒽
苯并[a]芘
茚并[1,2,3-cd]芘
二苯并[a,h]蒽
苯并[g,h,i]苝
吡啶
2-甲基吡啶
N-亚硝基甲基乙基胺
甲基磺酸甲酯
N-亚硝基二乙胺
甲基磺酸乙酯
联苯胺
五氯乙烷
苯甲醇
3-甲基苯酚
N-亚硝基吡咯烷
苯乙酮
N-亚硝基吗啉
邻甲苯胺
N-亚硝基哌啶
2,6-二氯苯酚
六氯丙烯
N-亚硝基二正丁胺
黄樟素
1,2,4,5-四氯苯
异黄樟素
N-亚硝基二苯胺
五氯苯
1-萘胺
2,3,4,6-四氯苯酚
2-萘胺
5-硝基邻甲苯胺
二苯胺
1,3,5-三硝基苯
非那西丁
4-氨基联苯
五氯硝基苯
美沙吡啉
对二甲基氨基偶氮苯
2-乙酰胺基芴
7，12-二甲基苯并蒽
苯酚
2-氯酚
2-硝基苯酚
2,4-二甲基苯酚
4-氯苯胺
4-氯3-甲酚
2-甲基萘
115-07-1
75-71-8
76-14-2
74-87-3
75-01-4
106-99-0
74-93-1
74-83-9
75-00-3
75-69-4
107-02-8
76-13-1
75-35-4
67-64-1
75-18-3
67-63-0
75-15-0
75-09-2
156-59-2
1634-04-4
110-54-3
75-34-3
108-05-4
78-93-3
156-60-5
141-78-6
109-99-9
67-66-3
71-55-6
110-82-7
56-23-5
71-43-2
107-06-2
142-82-5
79-01-6
78-87-5
80-62-6
123-91-1
75-27-4
10061-01-5
624-92-0
108-10-1
108-88-3
10061-02-6
79-00-5
127-18-4
591-78-6
124-48-1
106-93-4
108-90-7
100-41-4
"108-38-3/
106-42-3"
95-47-6
100-42-5
75-25-2
79-34-5
622-96-8
108-67-8
95-63-6
541-73-1
106-46-7
100-44-7
95-50-1
120-82-1
87-68-3
91-20-3
"""
    showinfo(compunds)
