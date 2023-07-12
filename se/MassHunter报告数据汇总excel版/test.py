import tkinter
import tkinter.filedialog
import tkinter.scrolledtext
import time

window=tkinter.Tk()#初始化
window.title('MassHunter报告数据汇总')#标题
window.geometry()#窗口范围

string1=tkinter.StringVar()#文本，用于显示在label等控件上
string1.set('输入or选择路径')#设置string的值
content_log=tkinter.scrolledtext.ScrolledText(font=('None',14),height=15)
content_log.pack(side='bottom',expand=True,fill='both')
content_log.insert('1.0','文件浏览记录:\n')
content_sort=tkinter.scrolledtext.ScrolledText(font=('None',14),height=15)
content_sort.pack(side='bottom',expand=True,fill='both')
content_sort.insert('1.0','自定义排序请将模板黏贴此处（beta）\n')
label=tkinter.Label(window,text='目标路径:',font=('None',14))#label控件
label.pack(side='left')#放置控件
ety_path=tkinter.Entry(window,textvariable=string1,font=('None',14))#输入框，可用Entry.get()取得输入的值
ety_path.pack(side='left',fill='x',expand=True)

def select():
    filepath=tkinter.filedialog.askopenfilename()#选择一个文件，取得他的绝对路径
    string1.set(filepath)
    content_log.insert('end', '[{}] {}\n'.format(time.strftime('%H:%M:%S'),filepath))
button_select=tkinter.Button(window,text='选择',font=('None',12),width=10,height=1,command=select)#注：command后的函数不可传入参数
button_select.pack(side='left')

def run():
    str=content_sort.get('1.0','end')
    print(str)
    l=str.split('将')
    print(l)
button_run=tkinter.Button(window,text='处理',font=('None',12),width=10,height=1,command=run)
button_run.pack(side='left')

menubar=tkinter.Menu(window)#以下部分为添加菜单
menu_first=tkinter.Menu(menubar)
menu_second=tkinter.Menu(menu_first)
menu_third=tkinter.Menu(menu_second)
menubar.add_cascade(label='一级菜单示例',menu=menu_first)
menu_first.add_cascade(label='二级菜单示例',menu=menu_second,underline=0)
menu_first.add_separator()
menu_first.add_command(label='打开',command=None)
menu_first.add_command(label='保存',command=None)
menu_first.add_separator()
menu_first.add_command(label='退出',command=window.quit)
menu_second.add_cascade(label='三级菜单示例',menu=menu_third)
menu_second.add_separator()
menu_second.add_command(label='打开',command=None)
menu_third.add_command(label='打开',command=None)
window.config(menu=menubar)

window.mainloop()