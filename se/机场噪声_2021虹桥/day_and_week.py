import day
import os
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)
if __name__ == '__main__':
    print('请将excel按点位归类，将此程序放在点位文件夹同级目录运行\n'
          '结果会保存在MySQL服务器(10.1.210.117, 3306,root, 123456, airport_noise)\n'
          '请确保已安装Microsoft Excel\n')
    path = os.getcwd()
    # path = r"C:\Users\Administrator\Desktop\噪声桌面\复算"
    print('正在计算')
    day.run_oneday_week(path)
    print('\n全部处理完成，按任意键退出')
    input()
