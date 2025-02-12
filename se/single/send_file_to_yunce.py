# -*- coding: utf-8 -*-
# date: 2024-12-4
"""
谱图文件上传到云测服务器
"""
import os.path
import base64
import re
import logging
import time

import win32clipboard
import ctypes
import requests
import pyperclip

logging.basicConfig(level=logging.DEBUG)


# logging.disable(level=logging.INFO)


def get_names_from_clickboard():
    """
    获取仪器名和批名,如果re有结果，更新变量值
    :return:
    """
    global equcode, batchcode, clickboard_text
    next_text = pyperclip.paste()
    if clickboard_text != next_text and next_text != '':  # 检测到文本更新
        clickboard_text = next_text  # 更新值
        debug_text = clickboard_text_ if len(
            clickboard_text_ := next_text.replace('\n', '').replace('\r', '')) <= 50 else clickboard_text_[:50] + '...'
        logging.debug(f'copied_text:{debug_text}')  # 输出更新的文本内容
        regx = re.compile(r'批次号：\s*(\w+).+?分析仪器：.+?(SEMTEC-\d+)', flags=re.DOTALL)
        if searchres := regx.search(clickboard_text):
            batchcode = searchres.group(1)
            equcode = searchres.group(2).replace('-', '_')
            logging.info(f'find_codes:({equcode},{batchcode})')


def get_filepaths_from_clickboard():
    """
    获取所有文件路径
    :return:
    """
    global filepaths, equcode, batchcode
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
        logging.debug(f'selected_files:{data}')
        filepaths = [fp for fp in data if os.path.isfile(fp)]
    except TypeError:
        pass
    finally:
        try:
            win32clipboard.CloseClipboard()
        except Exception:
            pass


def clear_clickboard():
    """
    清空剪贴板
    :return:
    """
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
    finally:
        try:
            win32clipboard.CloseClipboard()
        except Exception:
            pass


def init():
    """
    初始化变量，清空剪贴板
    :return:
    """
    global filepaths, equcode, batchcode, clickboard_text
    filepaths, equcode, batchcode = [], '', ''  # 初始化3个关键变量
    clickboard_text = ''  # 存放clickboard文本，如果发生改变，更新值然后reserch，避免重复检测。
    clear_clickboard()


def encode_file_to_base64(file_path):
    """
    将文件base64编码
    base64编码和返回的对象是bytes，decode后返回str
    :param file_path:
    :return:
    """
    with open(file_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode('utf-8')
    return encoded_string


def send_to_server(file_path, equipment_code, batch_code):
    """
    直接将文件发送到服务端
    requests发送的是bytes，requests会自动将str转bytes，但在遇到错误时需要手动将str encode为bytes
    :param file_path: 文件路径
    :param equipment_code: SEMTEC_212
    :param batch_code: FG2412419
    :return:
    """
    encoded_buffer = encode_file_to_base64(file_path)
    url = 'http://10.1.31.200:8000/AppModules/ApparatusInterface/ApparatusInterfaceService.asmx'
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; MS Web Services Client Protocol 4.0.30319.42000)",
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "http://tempuri.org/UploadApparatusFile",
        "Host": "10.1.31.200:8000"
    }

    body = f'''<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <soap:Body>
        <UploadApparatusFile xmlns="http://tempuri.org/">
          <token>etims@yunce</token>
          <buffer>{encoded_buffer}</buffer>
          <create_company_id>10141</create_company_id>
          <batch_code>{batch_code}</batch_code>
          <file_name>{os.path.split(file_path)[-1]}</file_name>
          <equipment_code>{equipment_code}</equipment_code>
          <file_parse_method>{equipment_code}</file_parse_method>
        </UploadApparatusFile>
      </soap:Body>
    </soap:Envelope>'''

    response = requests.post(url=url, headers=headers, data=body.encode('utf-8'))
    return response


def printinstructions():
    qrcode = '''||||||||||||||||||||||||||||||||||||||||||||||||||||||
||              ||||  ||||  ||||    ||              ||
||  ||||||||||  ||||||        ||    ||  ||||||||||  ||
||  ||      ||  ||      ||  ||||||  ||  ||      ||  ||
||  ||      ||  ||||      ||||||    ||  ||      ||  ||
||  ||      ||  ||||||  ||||||||    ||  ||      ||  ||
||  ||||||||||  ||||  ||||||||    ||||  ||||||||||  ||
||              ||  ||  ||  ||  ||  ||              ||
||||||||||||||||||      ||      ||  ||||||||||||||||||
||      ||          ||    ||||          ||||||  ||||||
||  ||||  ||||||  ||||    ||||||||||      ||||||||  ||
||||                  ||||||  ||||    ||||  ||      ||
||||    ||  ||||||||||||  ||||||          ||||||  ||||
||  ||||    ||    ||||||||  ||||||||||    ||  ||    ||
||||    ||||||||||||||||      ||||||||    ||  ||||  ||
||  ||||  ||    ||    ||    ||  ||  ||      ||      ||
||||        ||||    ||||||      ||||||||  ||  ||  ||||
||  ||||        ||    ||  ||||  ||            ||||||||
||||||||||||||||||  ||    ||||  ||  ||||||          ||
||              ||  ||  ||||  ||    ||  ||  ||||    ||
||  ||||||||||  ||  ||||  ||||||    ||||||    ||||  ||
||  ||      ||  ||    ||||  ||||||          ||||||  ||
||  ||      ||  ||||          ||      ||||  ||  ||||||
||  ||      ||  ||    ||    ||  ||  ||||||    ||||  ||
||  ||||||||||  ||  ||||||      ||  ||  ||    ||  ||||
||              ||    ||  ||||  ||  ||||  ||||||    ||
||||||||||||||||||||||||||||||||||||||||||||||||||||||
'''
    print(qrcode)
    print("坤坤谱图上传助手V1.0\n"
          "支持系统：Windows 10/11\n"
          "windows10下鼠标左键暂停程序，右键恢复程序，windows11不受影响。\n"
          "KunKun is my idol and I am an IKUN.\n"
          "Let's use KunKun_upload_tool instead of YunCeApp.\n")
    print('使用说明：\n'
          '1、在分析录入页面Ctrl+A，Ctrl+C复制所有文字;\n'
          '2、复制要上传的谱图文件（可多选），文件会自动上传。\n')


def disable_quickedit():
    """
    禁用控制台快速编辑
    :return:
    """
    # 获取控制台输入输出的句柄
    kernel32 = ctypes.windll.kernel32

    # 获取标准输入句柄
    stdin_handle = kernel32.GetStdHandle(-10)  # -10 表示标准输入

    # 获取当前控制台输入模式
    mode = ctypes.c_uint32()
    kernel32.GetConsoleMode(stdin_handle, ctypes.byref(mode))

    # 关闭快速编辑模式（0x0040是表示快速编辑模式的标志）
    new_mode = mode.value & ~0x0040  # 清除快速编辑模式的标志

    # 设置新的控制台模式
    kernel32.SetConsoleMode(stdin_handle, new_mode)


if __name__ == '__main__':
    # disable_quickedit()
    printinstructions()
    global filepaths, equcode, batchcode, clickboard_text
    init()
    while True:
        get_names_from_clickboard()  # 循环监测text
        time.sleep(0.4)  # 循环时间应<用户两次复制操作之间间隔的时间
        while equcode and batchcode:  # 读取到text后，改为监测文件
            time.sleep(0.5)
            get_filepaths_from_clickboard()
            if filepaths:
                for file in filepaths:
                    response = send_to_server(file_path=file, equipment_code=equcode, batch_code=batchcode)
                    logging.info(f'sent:{os.path.split(file)[-1]}, status_code:{response.status_code}')
                init()

#  pyinstaller 坤坤谱图上传助手.py -F -i kk.ico
