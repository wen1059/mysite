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
        logging.debug(f'{clickboard_text[:50].replace('\n', '').replace('\r', '')}...')  # 输出更新的文本内容
        regx = re.compile(r'批次号：\s*(\w+).+?分析仪器：.+?(SEMTEC-\d+)', flags=re.DOTALL)
        if searchres := regx.search(clickboard_text):
            batchcode = searchres.group(1)
            equcode = searchres.group(2).replace('-', '_')
            logging.info(f'{equcode}, {batchcode}')


def get_filepaths_from_clickboard():
    """
    获取所有文件路径
    :return:
    """
    global filepaths, equcode, batchcode
    if equcode and batchcode:  # 复制网页后才识别复制的文件，这样可以保证顺序，避免混乱
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
            filepaths = [fp for fp in data if os.path.isfile(fp)]
        except TypeError:
            pass
        finally:
            win32clipboard.CloseClipboard()


def clear_clickboard():
    """
    清空剪贴板，设置默认变量
    :return:
    """
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
    finally:
        win32clipboard.CloseClipboard()


def init():
    """
    初始化变量，清空剪贴板
    :return:
    """
    global filepaths, equcode, batchcode, clickboard_text
    clear_clickboard()
    filepaths, equcode, batchcode = [], '', ''
    clickboard_text = ''


def encode_file_to_base64(file_path):
    """
    将文件编码
    :param file_path:
    :return:
    """
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode('utf-8')
    return encoded_string


def send_to_server(file_path, equipment_code, batch_code):
    """

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


if __name__ == '__main__':
    filepaths, equcode, batchcode = [], '', ''  # 初始化3个关键变量
    clickboard_text = ''  # 存放clickboard文本，如果发生改变，更新值然后reserch，避免重复检测。
    while True:
        get_names_from_clickboard()
        get_filepaths_from_clickboard()

        if equcode and batchcode and filepaths:
            for file in filepaths:
                response = send_to_server(file_path=file, equipment_code=equcode, batch_code=batchcode)
                logging.info(f'{os.path.split(file)[-1]}, {response.status_code}')
            init()
        time.sleep(0.3)
