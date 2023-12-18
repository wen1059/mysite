"""
去除电子签png图片的白色背景
检测像素，RGB都为220以上的点设置透明度100%，可修改220数值来修改识别度。
"""
import os
import sys
from concurrent.futures import ProcessPoolExecutor

from PIL import Image


def genpng(rootpath):
    for root, _, files in os.walk(rootpath):
        for file in files:
            if file.lower().endswith(('.png', '.jpg')):
                yield os.path.join(root, file)


def dropwhite(pic: str):
    try:
        img = Image.open(pic).convert("RGBA")
    except Exception as e:
        print(pic, e)
        return
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            r, g, b, _ = img.getpixel((x, y))
            if r > 180 and g > 180 and b > 180:
                img.putpixel((x, y), (255, 255, 255, 0))
    img.save(pic + '_去底色.png')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        pngs = sys.argv[1:]
    else:
        path = os.path.split(os.path.realpath(__file__))[0]
        # path = r"C:\Users\Administrator\Pictures\Screenshots"
        pngs = genpng(path)
    with ProcessPoolExecutor() as pool:
        for png in pngs:
            pool.submit(dropwhite, png)
