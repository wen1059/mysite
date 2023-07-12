import cv2
import numpy as np
import os
import time
from PIL import Image


class Settings:
    def __init__(self):
        self.cols = 190  # 图片分割的列数
        self.scale = 3  # 字体高宽比,django{{ content|linebreaks }}渲染到html<code>标签字体设置3
        self.gscale = [r'$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzxvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`". ',
                       r'$%#*=+-:. ',
                       r'#. ']


def convert_frame_to_asc(frame):
    """
    转换单帧为字符码
    :param settings:
    :param frame: cv2的每一帧,ndarray格式
    :return: 字符串格式
    """

    def getaveL(image):
        """
        计算图片像素平均值
        :param image:
        :return:
        """
        im = np.array(image)
        w, h = im.shape
        return np.average(im.reshape(w * h))

    settings = Settings()
    image = Image.fromarray(frame).convert('L')
    W, H = image.size[0], image.size[1]
    w = W / settings.cols  # 裁剪的小图宽
    h = w * settings.scale  # 裁剪的小图高，高宽比保持和输出字体的高宽比一致
    rows = int(H / h)
    asc = ''
    for i in range(rows):
        for j in range(settings.cols):
            img = image.crop((int(j * w), int(i * h), int((j + 1) * w), int((i + 1) * h)))
            avgl = getaveL(img)
            s1 = settings.gscale[0][round(avgl / 255 * (len(settings.gscale[0]) - 1))]
            s2 = settings.gscale[1][round(avgl / 255 * (len(settings.gscale[1]) - 1))]
            asc += s2
        asc += '\n'
    asc += '\t'  # 把所有帧存在一起，\t作为帧之间的识别符
    return asc


def convert_video_to_ascs(video):
    """
    转换视频为asc，按帧的顺序保存到txt，\t作为帧之间的分隔符
    :param video:
    :return:
    """
    cap = cv2.VideoCapture(video)
    with open('test.txt', 'w') as f:
        while True:
            retval, frame = cap.read()  # frame是ndarray格式
            if not retval:
                break
            f.write(convert_frame_to_asc(frame))


def print_ascs(txt):
    """
    播放字符画
    :param txt: 预先转换后保存的txt文件
    :return:
    """
    with open(txt) as f:
        ascs = f.read()
        for i in ascs.split('\t'):
            os.system('cls')
            print(i)
            time.sleep(1 / 30)


if __name__ == '__main__':
    # convert_video_to_ascs('Alstroemeria.Records.-.[Bad.Apple!!.feat..nomico].(PV).mkv')
    print_ascs(r"C:\Users\Administrator\PycharmProjects\mysite\static\indextext\test2-2.txt")
