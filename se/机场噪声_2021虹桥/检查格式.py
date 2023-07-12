"""
添加缺失的背景干扰
删除多余的背景干扰
检查黏贴错位的地方，不修正
"""
import os
import xlwings

# print('注意：鼠标左键黑框会暂停运行, 右键黑框继续运行, 必须安装office，wps不行的\n')
# print('当显示“全部完成”即检查完毕，可以ctrl+a,ctrl+c复制出来\n')


def yieldsht(walkpath):
    """
    生成每个要处理的表
    :return:
    """
    app_24 = xlwings.App(visible=False, add_book=False)  # 待计算文件
    for root, _, files in os.walk(walkpath):
        for filexlsx in files:
            if filexlsx[-5:-1] != '.xls' or '~$' in filexlsx:
                continue
            file24path = os.path.join(root, filexlsx)
            file24 = app_24.books.open(file24path)  # 24小时文件
            yield file24.name, file24.sheets[0]
            file24.save()
            file24.close()
    app_24.quit()


for name, sht in yieldsht(r'\\bg\环境报告审核人共享\2017-2020报告\2020\浦东噪声\浦东数据汇总7.2'):
    for i in range(3, 2080):
        jx = sht.range(f'j{i}').value
        if jx in [None, '机型']:
            continue
        lepn = sht.range(f'd{i}').value
        beizhu = sht.range(f'n{i}').value
        ijklmn = sht.range(f'i{i}:m{i}').value
        if (lepn is None) and (beizhu is None):
            sht.range(f'n{i}').value = '背景干扰'
            print(name, i, '缺')
        elif lepn and beizhu:
            sht.range(f'n{i}').value = None
            print(name, i, '多')
        if None in ijklmn:
            print(name, i, '错位')
print('全部完成')
input()
