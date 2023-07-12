# -*- coding: utf-8 -*-
# date: 2023-2-3
import pyautogui
import random
import time


def run(cishu):
    """

    :param cishu: 刷屏次数
    :return:
    """
    for i in range(cishu):
        s = ''.join([chr(i) for i in range(1, 223)])  # 备选字库
        text = ''  # 每条刷屏的内容
        for t in range(random.randint(1, 3)):  # 随机字数
            text_ = random.choice(s)
            text += text_
        pyautogui.typewrite(text)
        pyautogui.hotkey('ctrlright', 'enter')


time.sleep(2)
run(1000)
