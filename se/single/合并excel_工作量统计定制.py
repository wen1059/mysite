import os
import traceback
from glob import glob

try:
    import xlwings
except ImportError:
    print('首次运行会下载依赖库，请耐心等待，若程序退出请重新运行一次。')
    os.system('pip install xlwings -i https://pypi.tuna.tsinghua.edu.cn/simple/')
    import xlwings
from xlwings.main import Book, Sheet


class MyException(Exception):
    pass


print('功能：将所有excel按月份合并到一个新的excel\n'
      '需要运行环境：Windows10/Microsoft Office\n')
path = os.getcwd()
# path = r"C:\Users\Administrator\Desktop\11 工作量统计"
os.chdir(path)
files = glob(path + r'\\**\\*.xlsx', recursive=True)
# files = glob(path + r'\\*.xlsx')
app = xlwings.App(visible=False, add_book=False)
for i in range(1, 13):  # 12个月份
    try:
        f_merge: Book = app.books.add()
        sht0: Sheet = f_merge.sheets[0]
        if os.path.exists(f'合并_{i}月.xlsx'):  # 此条决定覆盖还是跳过
            print(f'合并_{i}月.xlsx已存在，跳过合并')
            raise MyException
        flag = True
        for file in files:
            if '~' in file or '合并' in file or '模板' in file:
                continue
            xlsx: Book = app.books.open(file)
            flag = False
            sht: Sheet
            for sht in xlsx.sheets:
                if str(i) in sht.name:
                    sht.copy(before=sht0, name=xlsx.name.strip('.xlsx'))
                    print(f'正在合并{sht}')
                    flag = True
                    break  # 找到这个sheet就不往下找了
            if not flag:  # 如果第一个文件没有这个月份，那么flag=False，不接着读下个文件。
                print(f'[ERROR] {os.path.basename(file)}无{i}月，终止合并{i}月')
                raise MyException
            xlsx.close()
        if f_merge.sheets.count != 1:  # sheet数量==1表示没有这个月份，不保存合并文件
            sht0.name = '总数加和'
            sht0.range('a1').options(transpose=True).value = f_merge.sheets[0].range('a1:a34').value
            for j in range(3, 35):
                sht0.range(f'b{j}').formula = f"=sum('*'!b{j})"
            f_merge.save(f'合并_{i}月.xlsx')
        f_merge.close()
    except MyException:
        pass
    except Exception:
        traceback.print_exc()
app.quit()
print('\n合并完成，文件保存在“合并_{ }月.xlsx”')
os.system('pause')
# 合并excel_工作量统计定制.py -F
