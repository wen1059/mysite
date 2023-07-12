from PIL import Image
import numpy as np

gscale1 = r'$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzxvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`". '
gscale2 = r'@%#*=+-:. '


class Settings:
    def __init__(self):
        self.cols = 300
        self.scale = 0.5
        # self.gs1=True
        self.gs1 = False


setting = Settings()
pic = r"C:\Users\Administrator\PycharmProjects\se\projectcode\pic-asc2\test.jpg"
image = Image.open(pic).convert('L')
W, H = image.size[0], image.size[1]
w = W / setting.cols
h = w / setting.scale
rows = int(H / h)


def getaveL(image):
    im = np.array(image)
    w, h = im.shape
    return np.average(im.reshape(w * h))


asclist = []
for i in range(rows):
    asclist.append('')
    for j in range(setting.cols):
        img = image.crop((int(j * w), int(i * h), int((j + 1) * w), int((i + 1) * h)))
        avgl = getaveL(img)
        if setting.gs1:
            gs = gscale1[int(avgl * 69 / 255)]
        else:
            gs = gscale2[int(avgl * 9 / 255)]
        asclist[i] += gs

with open(r"C:\Users\Administrator\PycharmProjects\se\projectcode\pic-asc2\test.txt", 'w') as f:
    for i in range(len(asclist)):
        f.write(asclist[i] + '\n')
