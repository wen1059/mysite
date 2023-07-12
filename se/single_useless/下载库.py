print('\n正在下载依赖库，请不要关闭此窗口\n')
import os, getpass
username = getpass.getuser()
pippath = r'c:\users\{}\pip'.format(username)
if not os.path.exists(pippath):
    os.mkdir(pippath)
with open(r'{}\pip.ini'.format(pippath), 'w') as f:
    f.write('[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple')
os.system('pip install xlwings numpy pillow pyautogui')
print('\n下载完成，可以关闭此窗口')
input()
