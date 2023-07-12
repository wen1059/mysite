import os
folderpath=''
name=''
# insname=''

def addname(path,name):
    for root,_,files in os.walk(path,name):
        for oldname in files:
            if oldname[-4:]=='.AWA' and (name not in oldname):
                newname=oldname.replace('.AWA',name+'.AWA')
                os.rename(os.path.join(root,oldname),os.path.join(root,newname))
                global insname,content_log
                # insname+='{} --> {}\n'.format(oldname,newname)
                content_log.insert('end','{} --> {}\n'.format(oldname,newname))

import tkinter
import tkinter.filedialog
import tkinter.scrolledtext

window=tkinter.Tk()
window.title('LT文件添加姓名')
window.geometry('')

content_log=tkinter.scrolledtext.ScrolledText(font=('None',14),width=58,height=27)
content_log.pack(side='bottom')

label=tkinter.Label(window,text='1、输入姓名:',font=('None',14))#label控件
label.pack(side='left')#放置控件
# string1=tkinter.StringVar()#文本，用于显示在label等控件上
# string1.set('输入姓名')#设置string的值
ety_path=tkinter.Entry(window,textvariable=None,font=('None',14))#输入框，可用Entry.get()取得输入的值
ety_path.pack(side='left',fill='x',expand=False)

def select():
    global folderpath
    folderpath = tkinter.filedialog.askdirectory()
    content_log.delete('1.0','end')
    content_log.insert('end','已选择文件夹  {}\n'.format(folderpath))
button_select=tkinter.Button(window,text='2、选择文件夹',font=('None',12),width=15,height=1,command=select)
button_select.pack(side='left')

def run():
    name=ety_path.get()
    addname(folderpath,name)
    content_log.insert('end', '完成\n')
button_run=tkinter.Button(window,text='3、添加姓名',font=('None',12),width=15,height=1,command=run)
button_run.pack(side='left')

window.mainloop()
