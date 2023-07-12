from PIL import Image
import zipfile
import os
import xlwings
from itertools import islice


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
            yield file24path, file24.sheets[0]
            file24.close()
    app_24.kill()


def gen_pic(xlspath):
    zf = zipfile.ZipFile(xlspath, 'r')
    for i in range(1, 25):
        xlspic = zf.open(f'xl/media/image{i}.png')
        yield xlspic


def count_blue(xlspic):
    """
    统计蓝峰个数，
    :param xlpath:
    :return: 24张图片蓝峰数的列表
    """
    pink = (240, 158, 159, 255)
    blue = (0, 0, 255, 255)
    pic = Image.open(xlspic)
    # pic.show()
    w, h = pic.size

    def find_pink():
        """
        找到粉色的最底处
        :return:往上高10个像素
        """
        for h_ in reversed(range(h)):
            if pic.getpixel((int(w / 2), h_)) in (pink, blue):
                return h_
        return 0

    hh = find_pink()
    count = 0
    pix_next = pic.getpixel((0, hh))
    for w_ in range(1, w, 2):
        pix, pix_next = pix_next, pic.getpixel((w_, hh))
        if pix_next == blue and pix != blue:
            count += 1
    return count


def count_sj(sht):
    """
    统计事件数，
    :return: 24个时段事件个数的列表
    """
    res=[]
    count1=0
    for i in range(6, 2080):
        a=sht.range(f'a{i}').value
        if a=='startTime':
            count1=0
        elif str(a[0]).isdigit():
            count1+=1
        elif a=='监测开始时间':
            res.append(count1)
    return res


for xlspath, sht in yieldsht(r"C:\Users\Administrator\Desktop\新建文件夹"):
    blue=[count_blue(pic) for pic in gen_pic(xlspath)]
    sj=count_sj(sht)

