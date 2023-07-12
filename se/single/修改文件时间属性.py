import os,time
def changefiletime(awafilepath,newatime,newmtime):
    '''
    :param awafilepath: awa文件路径
    :param newatime: 访问时间
    :param newmtime: 修改时间
    :return: /
    '''
    nat = time.strptime(newatime, '%Y-%m-%d %H:%M:%S')  # 时间解析为tumple
    nat = time.mktime(nat)  # 时间改为时间戳
    nmt=time.strptime(newmtime, '%Y-%m-%d %H:%M:%S') # 时间解析为tumple
    nmt=time.mktime(nmt) # 时间改为时间戳
    os.utime(awafilepath,(nat,nmt)) # 修改(atime,mtime)

awafilepath = r'd:\test\1.txt'
newatime = '2020-09-29 13:50:22'
newmtime = '2020-09-29 13:50:22'

changefiletime(awafilepath,newatime,newmtime)