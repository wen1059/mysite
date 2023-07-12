import numpy
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D


def draw3d(file, threshold, RT, mz_low, mz_high, tic=True):
    fig = pyplot.figure(figsize=(10, 8))
    ax = Axes3D(fig)
    arr = numpy.loadtxt(file, delimiter=',')
    for i in range(1, arr.shape[1]):  # 先固定y轴，逐个碎片离子绘图
        if mz_low < arr[0, i] < mz_high:  # 设置要绘制的M/Z范围
            x = []
            z = []
            for j in range(1, arr.shape[0]):
                if arr[j, i] >= threshold and arr[j, 0] < RT:  # 基线过滤和选择RT范围
                    x.append(arr[j, 0])
                    z.append(arr[j, i])
            y = []
            y.append(arr[0, i])
            y *= len(x)
            ax.plot(x, y, z)
    if tic:
        x = arr[1:, 0]
        y = [mz_high + 1] * len(x)
        z = arr[1:, -1]
        ax.plot(x, y, z)
    ax.set_title('三维质谱图', fontproperties='SimSun')
    ax.set_xlabel('时间', fontproperties='SimSun')
    ax.set_ylabel('M/Z')
    ax.set_zlabel('丰度', fontproperties='SimSun')
    pyplot.show()


draw3d(r'c:\ttmp\123.csv', threshold=0, RT=15, mz_low=55, mz_high=65, tic=False)
