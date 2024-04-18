# -*- coding: utf-8 -*-
# date: 2024-3-25
"""
绘制一张渐变色图片,从圆心开始逐渐淡出
"""
from PIL import Image
import math


class DrawGradient:
    def __init__(self, size=(1024, 1024)):
        self.im = Image.new('RGBA', size, (0, 0, 0, 0))
        self.basecolor = (161, 196, 253)
        self.othercolor = [(161, 196, 253),  # 圆心的颜色
                           (255, 228, 225)
                           ]

    def put_scaled_pixel(self, x, y, basecolor):
        # point = (x, y)  # 像素点坐标
        # 像素点到圆心的距离，绘制圆形扩散
        distance = math.sqrt(math.pow((self.im.size[0] / 2 - x), 2) + math.pow((self.im.size[1] / 2 - y), 2))
        # distance = max(abs(self.im.size[0] / 2 - x), abs(self.im.size[1] / 2 - y))  # 绘制正方形扩散
        percentage = distance / (self.im.size[0] / 2)  # 距离和半径的比值，用来判断rgb值渐变的百分比，离圆心越远，颜色越淡
        # 根据到圆心的距离计算到的渐变过的rgb值,透明度为255
        color_scaled = tuple(int(i + (255 - i) * percentage) for i in basecolor[:-1]) + (255,)
        # if percentage <= 1:  # 超出园半径的区域不绘图，保持透明
        self.im.putpixel((x, y), color_scaled)

    def drawpic(self):
        for x in range(self.im.size[0]):
            for y in range(self.im.size[1]):
                self.put_scaled_pixel(x, y, self.basecolor)

    def drawhalfpic(self):
        for x in range(int(self.im.size[0] / 2)):
            for y in range(int(self.im.size[1])):
                self.put_scaled_pixel(x, y, self.othercolor[0])
        for x in range(int(self.im.size[0] / 2), self.im.size[0]):
            for y in range(int(self.im.size[1])):
                self.put_scaled_pixel(x, y, self.othercolor[1])


if __name__ == '__main__':
    dg = DrawGradient()
    dg.drawpic()
    dg.im.show()
