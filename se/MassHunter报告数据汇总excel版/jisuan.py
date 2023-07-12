def cal(fu_o):
    fu=str(fu_o)
    result=fu[0]
    for i in range(1,len(fu)):
        if fu[i].isupper():
            result+="+"+fu[i]
        elif fu[i].islower():
            result += fu[i]
        elif fu[i].isdigit():
            result+='*'+fu[i]
    C,H,O,N,Cl,Br,S,F=12,1,16,14,35,79,32,18
    cal_result=eval(result)
    return cal_result

#以下部分为gui
import tkinter

window=tkinter.Tk()#初始化
window.title('分子量计算')#标题
window.geometry()#窗口范围

string1=tkinter.StringVar()#文本，用于显示在label等控件上

label=tkinter.Label(window,text='请输入分子式:',font=('None',14))#label控件
label.pack(side='left')#放置控件
ety_path=tkinter.Entry(window,textvariable=string1,font=('None',14))#输入框，可用Entry.get()取得输入的值
ety_path.pack(side='left',fill='x',expand=True)
text=tkinter.Text()
text.pack(side='right')

def run():
    text.insert('end','{}: {}\n'.format(ety_path.get(),cal(fu_o=ety_path.get())))
button_run=tkinter.Button(window,text='计算',font=('None',12),width=10,height=1,command=run)
button_run.pack(side='left')

window.mainloop()
