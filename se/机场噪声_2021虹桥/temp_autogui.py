from mypkg.walk import Walk
import pyautogui
import os
import time

w = Walk(filetype='xlsx', path=r"C:\Users\Administrator\Desktop\虹桥噪声桌面\浦东优先分析点位\old")
for file in w.filepaths:
    os.startfile(file)
    time.sleep(1)
    pyautogui.press('left')

    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 's')
    time.sleep(0.5)
    pyautogui.press('tab', 6)
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.press('left')

    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.hotkey('alt', 'f4')
