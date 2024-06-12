# -*- coding: utf-8 -*-
# date: 2023-12-13
import os.path
import sys

import cv2
import numpy as np
import xlwings
from xlwings.main import Book, Sheet


def calculate_average_rgb_squares(image_path: str, columns: int) -> np.ndarray:
    """
    将图像裁剪成指定列数的正方形小块，并计算每块的平均RGB值。# GPT生成

    参数:
        image_path (str): 图像文件的路径。
        columns (int): 正方形块的列数。

    返回:
        square_averages (np.ndarray): 包含每块平均RGB值的二维数组。

    """
    # 读取图像,-1表示以bgra模式读取
    image = cv2.imread(image_path, -1)

    # 检查图像是否成功加载
    if image is None:
        raise ValueError("无法加载图像，请检查文件路径是否正确。")

    # 获取图像的尺寸
    height, width, _ = image.shape

    # 计算正方形块的边长，以及行数
    block_size = width / columns
    rows = int(height / block_size)

    # 初始化包含每块平均RGB值的数组
    square_averages = np.zeros((rows, columns, 4), dtype=int)

    # 遍历每块
    for i in range(rows):
        for j in range(columns):
            # 计算当前块的边界
            y1 = int(i * block_size)
            y2 = int((i + 1) * block_size)
            x1 = int(j * block_size)
            x2 = int((j + 1) * block_size)

            # 裁剪当前块
            square = image[y1:y2, x1:x2]

            # 计算当前块的平均RGB值
            average_color = np.mean(square, axis=(0, 1)).astype(int)

            # 存储平均RGB值
            square_averages[i, j] = average_color

    return square_averages


def setcolor(image_path, columns):
    """
    将像素设置为excel背景色
    :param columns: 图片分割的列数，数值越大，填充的单元格越多，图像越清晰。100列以上比较清晰。建议50-200
    :param image_path: 图片路径
    :return:
    """
    app = xlwings.App(visible=True, add_book=False)
    file = app.books.add()
    sht: Sheet = file.sheets[0]
    sht.range((1, 1), (1, columns)).column_width = 1.75  # 调整列宽设置单元格为正方形
    # 页面缩放。1080p显示器，图片分成90列，差不多是100%填满横向，根据需求调整。已设置自动
    app.api.ActiveWindow.Zoom = 100 * 50 / columns  # 设置50列100%显示
    square_averages = calculate_average_rgb_squares(image_path, columns)
    # 按顺序填充背景
    rows, columns, _ = square_averages.shape
    for i in range(rows):
        for j in range(columns):
            # opencv读取的是bgr顺序，改成rgb写入excel
            b, g, r, a = square_averages[i, j]
            #  白色留空，不涂底色，达到透明效果
            white: bool = r > 240 and g > 240 and b > 240
            #  png空白不做处理会被识别成黑色
            blank: bool = a == 0
            if not (white or blank):
                sht[i, j].color = (r, g, b)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        img = sys.argv[1]
    else:
        # img = os.path.split(os.path.realpath(__file__))[0]
        img = r"C:\Users\Administrator\Pictures\111.png"
    setcolor(img, 30)
