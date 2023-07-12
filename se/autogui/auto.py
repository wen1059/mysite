import pyautogui
import os

mx, my = None, None
folderpath = None
filename = []


def getfilename(folderpath):
    for *_, files in os.walk(folderpath):
        for file in files:
            if '.msp' in file:
                filename.append(file)


def ptpdf():
    # pyautogui.hotkey('altleft','tab')
    for i in range(len(filename)):
        pyautogui.click(mx, my)
        pyautogui.typewrite(filename[i])
        pyautogui.press('enter')
        pyautogui.PAUSE = 3
        pyautogui.press('down')
        content_log.insert('1.0', '{}、{}'.format(i + 1, filename[i]))


import tkinter
import tkinter.filedialog
import tkinter.scrolledtext

window = tkinter.Tk()
window.title()
window.geometry()

content_log = tkinter.scrolledtext.ScrolledText(font=('None', 14), height=15)
content_log.pack(side='bottom')


def select():
    folderpath = tkinter.filedialog.askdirectory()
    content_log.insert('end', folderpath)


button_select = tkinter.Button(window, text='1、选择文件夹', font=('None', 12), width=15, height=1, command=select)
button_select.pack(side='left')


def run():
    getfilename(folderpath=folderpath)
    ptpdf()


button_run = tkinter.Button(window, text='2、开始处理', font=('None', 12), width=15, height=1, command=run)
button_run.pack(side='left')

window.mainloop()
