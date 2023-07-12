import xlwings


def code(path):  # 主功能代码
    app = xlwings.App(visible=True, add_book=False)
    file1 = app.books.open(path)
    len_org = len(file1.sheets)  # 初始的sheet数量
    file1.sheets.add(after=file1.sheets[-1])  # 添加一个sheet放最后
    sht_last = file1.sheets[-1]
    try:
        index_options = file1.sheets[
                            'Options'].index - 1  # sheet<Options>（已被隐藏）的索引，为了处理在前面添加过sheet导致的错误，xlwings的索引从1开始，所以-1和list保持一致
    except:
        index_options = 0
    rng = file1.sheets[index_options + 1].range('a16').expand()  # 从a16展开，为了获取行数和列数
    rng_rows = rng.rows.count  # 统计行数
    # rng_cols=rng.columns.count#统计列数
    sht_last[1, 2].options(transpose=True).value = file1.sheets[index_options + 1].range(
        'a16:a{}'.format(rng_rows + 16)).value  # 导出化合物名称到第3列
    sht_last[0, 2].value = '化合物'
    count_0 = 0
    for i in range(index_options + 1, len_org - 1):
        if str(file1.sheets[i].name)[0:-2] == str(file1.sheets[i].range('d7').value)[0:-2]:  # 自行添加的sheet不导出数据
            sht_last[0, i + 2 - index_options - count_0].value = file1.sheets[i].name  # 导出sheet名称（样品编号）到第一行
            sht_last[1, i + 2 - index_options - count_0].options(transpose=True).value = file1.sheets[i].range(
                'f16:f{}'.format(rng_rows + 16)).value  # 导出对应的数据
        else:
            count_0 += 1  # 修正

    table = sht_last.range('c1').expand()  # 统计要删除第几行
    table_rows = table.rows.count
    delete_rows = []
    for i in range(table_rows - 1):
        if sht_last[i, 2].value in ['Compound', '4-溴氟苯(surr)']:
            delete_rows.append(i + 1)
    count_1 = 0
    for i in delete_rows:
        sht_last.api.rows('{}'.format(i - count_1)).delete  # 调用excel的API完成
        count_1 += 1  # 每删除1行后面的所有行会向上，所以-count来修正

    rows_final = table_rows - len(delete_rows)  # 删除不需要的行后最终的行数
    list_unsorted = sht_last.range('c2:c{}'.format(rows_final)).value
    if list_unsorted[0] in content_sort.get('1.0', 'end'):
        list_manual_sort = content_sort.get('1.0', 'end').splitlines()
    else:
        list_manual_sort = list_unsorted
    for i in range(len(list_unsorted)):
        sht_last.range('a{}'.format(i + 2)).value = list_manual_sort.index(list_unsorted[i]) + 1  # 查找a列表中的项在b列表的索引
    sht_last.range('b1').value = '原始排序'
    sht_last.range('b2').options(transpose=True).value = [i for i in range(1, rows_final)]  # 按顺序添加第一列序号
    sht_last.range('a1').value = 0
    sht_last.range('a1').api.Sort(Key1=sht_last.range('a1').api, Order1=1)  # 调用api，按照a列排序，Order1=1升序，=2降序
    sht_last.range('a1').value = '自定义排序'


# 以下部分为gui
import tkinter
import tkinter.filedialog
import tkinter.scrolledtext
import time

window = tkinter.Tk()  # 初始化
window.title('MassHunter报告数据汇总')  # 标题
window.geometry()  # 窗口范围

string1 = tkinter.StringVar()  # 文本，用于显示在label等控件上
string1.set('输入or选择路径')  # 设置string的值
content_log = tkinter.scrolledtext.ScrolledText(font=('None', 14), height=15)
content_log.pack(side='bottom', expand=True, fill='both')
content_log.insert('1.0', '文件浏览记录:\n')
content_sort = tkinter.scrolledtext.ScrolledText(font=('None', 14), height=15)
content_sort.pack(side='bottom', expand=True, fill='both')
content_sort.insert('1.0', '自定义排序请将模板黏贴此处（beta）')
label = tkinter.Label(window, text='目标路径:', font=('None', 14))  # label控件
label.pack(side='left')  # 放置控件
ety_path = tkinter.Entry(window, textvariable=string1, font=('None', 14))  # 输入框，可用Entry.get()取得输入的值
ety_path.pack(side='left', fill='x', expand=True)


def select():
    filepath = tkinter.filedialog.askopenfilename()  # 选择一个文件，取得他的绝对路径
    # Folderpath = tkinter.filedialog.askdirectory()  # 获得文件夹路径
    string1.set(filepath)
    content_log.insert('end', '[{}] {}\n'.format(time.strftime('%H:%M:%S'), filepath))


button_select = tkinter.Button(window, text='选择', font=('None', 12), width=10, height=1,
                               command=select)  # 注：command后的函数不可传入参数
button_select.pack(side='left')


def run():
    code(path=ety_path.get())


button_run = tkinter.Button(window, text='处理', font=('None', 12), width=10, height=1, command=run)
button_run.pack(side='left')

menubar = tkinter.Menu(window)  # 以下部分为添加菜单栏，保留功能扩展
menu_first = tkinter.Menu(menubar)
menu_second = tkinter.Menu(menu_first)
menu_third = tkinter.Menu(menu_second)
menubar.add_cascade(label='一级菜单示例', menu=menu_first)
menu_first.add_cascade(label='二级菜单示例', menu=menu_second, underline=0)
menu_first.add_separator()
menu_first.add_command(label='打开', command=None)
menu_first.add_command(label='保存', command=None)
menu_first.add_separator()
menu_first.add_command(label='退出', command=window.quit)
menu_second.add_cascade(label='三级菜单示例', menu=menu_third)
menu_second.add_separator()
menu_second.add_command(label='打开', command=None)
menu_third.add_command(label='打开', command=None)
window.config(menu=menubar)

window.mainloop()
