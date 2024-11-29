# -*- coding: utf-8 -*-
# date: 2024-7-10

# 1）ftp登陆连接
#
# from ftplib import FTP            #加载ftp模块
# ftp=FTP()                         #设置变量
# ftp.set_debuglevel(2)             #打开调试级别2，显示详细信息
# ftp.connect("IP","port")          #连接的ftp sever和端口
# ftp.login("user","password")      #连接的用户名，密码
# print ftp.getwelcome()            #打印出欢迎信息
# ftp.cmd("xxx/xxx")                #进入远程目录
# bufsize=1024                      #设置的缓冲区大小
# filename="filename.txt"           #需要下载的文件
# file_handle=open(filename,"wb").write #以写模式在本地打开文件
# ftp.retrbinaly("RETR filename.txt",file_handle,bufsize) #接收服务器上文件并写入本地文件
# ftp.set_debuglevel(0)             #关闭调试模式
# ftp.quit()                        #退出ftp
# 2）ftp相关命令操作
#
# ftp.cwd(pathname)                 #设置FTP当前操作的路径
# ftp.dir()                         #显示目录下所有目录信息
# ftp.nlst()                        #获取目录下的文件
# ftp.mkd(pathname)                 #新建远程目录
# ftp.pwd()                         #返回当前所在位置
# ftp.rmd(dirname)                  #删除远程目录
# ftp.delete(filename)              #删除远程文件
# ftp.rename(fromname, toname)#将fromname修改名称为toname。
# ftp.storbinaly("STOR filename.txt",file_handel,bufsize)  #上传目标文件
# ftp.retrbinary("RETR filename.txt",file_handel,bufsize)  #下载FTP文件


from ftplib import FTP
from uuid import uuid4
import os
import sys
import re
import pyperclip


def getnames():
    """
    获取仪器名和批名
    :return:
    """
    text = pyperclip.paste()
    regx = re.compile(r'批次号：\s*(\w+).+?分析仪器：.+?(SEMTEC-\d+)', flags=re.DOTALL)
    insname = regx.search(text).group(1)
    batchnane = regx.search(text).group(2).replace('-', '_')
    return insname, batchnane


def sendtoftp():
    ftp = FTP()
    ftp.encoding = 'gbk'
    ftp.connect('10.1.210.119')
    ftp.login(user='', passwd='')
    instrumentname = os.path.split(__file__)[1].split('.')[0]
    # instrumentname = 'SEMTEC_212'
    batch = pyperclip.paste()
    files = sys.argv[1:]

    ftp.cwd(instrumentname)
    # 删除旧批文件夹
    for oldbatch in ftp.nlst():
        try:
            ftp.rmd(oldbatch)
        except Exception:
            ftp.delete(oldbatch)

    # 建立新批文件夹
    ftp.mkd(batch)
    for file in files:
        with open(file, 'rb') as f:
            ftp.storbinary(rf'STOR .\{batch}\{str(uuid4()) + os.path.split(file)[-1]}', f)
    ftp.quit()


sendtoftp()
