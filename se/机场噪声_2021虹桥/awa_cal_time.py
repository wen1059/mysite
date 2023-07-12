import os
import re
import pymysql
import traceback
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)

class Mysqldb:
    """使用此类需要预先在mysql建立好库和表"""

    def __init__(self):
        self.con = pymysql.connect(host='localhost',
                                   port=3306,
                                   user='root',
                                   passwd='123456',
                                   database='airport_noise'
                                   )
        self.curse = self.con.cursor()

    def ins_to_tab(self, tab, values):
        """
        写入表，insert语句根据表名和values中元素做调整
        :param tab:要写入的表
        :param values: 需要写入的值，列表形式
        :return:
        """
        sql = '''INSERT INTO {} 
            ( pri, 点位, 日期, 校准时间 ) 
            VALUES 
            (NULL, \'{}\', \'{}\', \'{}\')''' \
            .format(tab, values[0], values[1], values[2])
        self.curse.execute(sql)
        self.con.commit()

res_=(0,0,0)
db = Mysqldb()
regx_file = re.compile(r'(\d{1,2}#{1,2})(....)..\.AWA')
regx_time = re.compile('Calibrate@....-..-.. (..:..:..) Lx=')
path = os.getcwd()
# path = r"C:\Users\Administrator\Desktop\新建文件夹"
for root, _, files in os.walk(path):
    for file in files:
        try:
            if ('.AWA' not in file) or ('#' not in file):
                continue
            dw = regx_file.search(file).group(1)
            date = regx_file.search(file).group(2)
            with open(os.path.join(root, file),encoding='utf-8',errors='ignore') as f:
                txt = f.readlines()
                # print(txt)
                cal = txt[2]
                caltime = regx_time.search(cal).group(1)
            res = (dw, date, caltime)
            # print(res_,res)
            if res==res_:
                continue
            # print(res)
            db.ins_to_tab('校准时间', res)
            res_=res
            break
        except Exception as e:
            print(e)
            traceback.print_exc()
            continue