import os
import time
import re


# def getfiletime(pathfile):
#     '''
#     返回文件时间：#YYDDHH
#     :param pathfile: awa绝对路径
#     :return:
#     '''
#     ft = os.path.getmtime(pathfile)  # mtime修改时间，ctime创建时间
#     ft = time.ctime(ft)  # 格式化时间
#     # print(ft)
#     yue = ft[-20:-17]  # 如Oct
#     timename = ft[-20:-11].replace(' ', '')
#     tndict = {'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11'}
#     timename = '#' + timename.replace(yue, tndict[yue])  # Oct替换成10
#     if len(timename) == 6:
#         timename = timename.replace('#{}'.format(tndict[yue]), '#{}0'.format(tndict[yue]))  # 101改1001
#     # print(timename)
#     return timename


def getfiletime2(pathfile):
    """
    更新方法
    :param pathfile:
    :return:
    """
    ft0 = os.path.getmtime(pathfile)
    ft = time.localtime(ft0)
    gshtime = time.strftime('%m%d%H', ft)
    # print(gshtime)
    return gshtime


def getfoldername(pathfile):
    """
    返回点位号:__,根据文件夹做适当修改
    :param pathfile: awa绝对路径
    :return:
    """
    regex = re.compile(r'\\.+\\(.+)\\.+\\.+AWA')  # 根据目录层次适当修改
    loca = regex.findall(pathfile)
    # print(loca)
    foldername = str(loca[0])
    if '#' in foldername:
        return foldername
    else:
        return foldername + '#'


def rename(walkpath):
    for root, _, files in os.walk(walkpath):
        for file in files:
            if file[0] in ['L', 'S'] and file[-4:] == '.AWA':
                foldername = getfoldername(os.path.join(root, file))
                filetime = getfiletime2(os.path.join(root, file))
                newname = ''
                if file[0] == 'L':
                    newname = foldername + filetime + '.AWA'
                elif file[0] == 'S':
                    newname = foldername + filetime + '-背景' + '.AWA'
                # print(newname)
                try:
                    # pass
                    os.rename(os.path.join(root, file), os.path.join(root, newname))
                except:
                    print('error:', os.path.join(root, file))
            elif (file[0:3] in ['1_3', 'NUM'] and file[-4:] == '.AWA') or (file[0:3] == 'IND'):  # 删除其余文件
                os.remove(os.path.join(root, file))
    print('finish')  # 控制台运行暂停查看状态
    input()


def rename_nobj(walkpath):
    for root, _, files in os.walk(walkpath):
        for file in files:
            if file[0] in ['L'] and file[-4:] == '.AWA':
                foldername = getfoldername(os.path.join(root, file))
                filetime = getfiletime2(os.path.join(root, file))
                newname = foldername + filetime + '.AWA'
                # print(newname)
                try:
                    # pass
                    os.rename(os.path.join(root, file), os.path.join(root, newname))
                except Exception as e:
                    print('error:', os.path.join(root, file))
            elif (file[0:3] in ['1_3', 'NUM', 'STA'] and file[-4:] == '.AWA') or (file[0:3] == 'IND'):  # 删除其余文件
                os.remove(os.path.join(root, file))
    print('finish')  # 控制台运行暂停查看状态
    input()


if __name__ == '__main__':
    print(os.getcwd())
    rename_nobj(
        os.getcwd()
    )
