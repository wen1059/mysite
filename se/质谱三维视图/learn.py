# # import matplotlib.pyplot as plt
# # x_value=list(range(-100,100))
# # y_value=[x**2 for x in x_value]
# # plt.figure(figsize=(10,6))
# # plt.plot(x_value,y_value)
# # plt.title('Square Numbers',fontsize=24)
# # plt.xlabel('Value',fontsize=14)
# # plt.ylabel('Square of Value',fontsize=14)
# # plt.tick_params(axis='both',labelsize=14)
# # plt.show()
# #
# # from random import randint
# # class Die():
# #     def __init__(self,numsides=6):
# #         self.numsides=numsides
# #     def roll(self):
# #         return randint(1,self.numsides)
# # die=Die()
# # results=[]
# # for i in range(1000):
# #     results.append(die.roll())
# # num_counts=[]
# # for i in range(die.numsides):
# #     num_counts.append(results.count(i+1))
# #
# # import pygal
# # hist=pygal.Bar()
# # hist.title='Rest 1000'
# # hist.x_labels=list(i for i in range(die.numsides))
# # hist.x_title='Result'
# # hist.y_title='F o R'
# # hist.add('D6',num_counts)
# # # hist.render_to_file('die.svg')
# #
# # import csv
# # file=r'c:\ttmp\123.tic'
# # with open(file) as f:
# #     l=csv.reader(f,delimiter='\t')
# #
# #     for i in l:
# #         l1 = []
# #         for j in i:
# #             try:
# #                 l1.append(float(j))
# #             except:
# #                 l1.append(j)
# #         print(l1)
# #
# #
# import numpy
# from matplotlib import pyplot
# from mpl_toolkits.mplot3d import Axes3D
#
# file=r'c:\ttmp\1234.csv'
# arr=numpy.loadtxt(file,delimiter=',')
# fig = pyplot.figure()
# ax = Axes3D(fig)
#
# for i in range(1,arr.shape[1]):
#     x=arr[1:,0]
#     y = []
#     y.append(arr[0,i])
#     y=y*len(x)
#     z=arr[1:,i]
#     print(y,type(y))
# import numpy
# from matplotlib import pyplot
# from mpl_toolkits.mplot3d import Axes3D
#
# def draw3d(file,threshold,RT,mz_low,mz_high,tic=True):
#     fig = pyplot.figure(figsize=(10,8))
#     ax = Axes3D(fig)
#     x=numpy.arange(-100,100)
#     y=x.copy()
#     def f(x,y):
#         return -x**3-y**3
#     x,y=numpy.meshgrid(x,y)
#     ax.plot_surface(x,y,f(x,y))
#
#     pyplot.show()
#
# draw3d(r'c:\ttmp\123.csv',threshold=0,RT=15,mz_low=55,mz_high=65,tic=False)
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)
len = 8;
step = 0.4;


def build_layer(z_value):
    x = np.arange(-len, len, step);
    y = np.arange(-len, len, step);
    z1 = np.full(x.size, z_value/2)
    z2 = np.full(x.size, z_value/2)
    z1, z2 = np.meshgrid(z1, z2)
    z = z1 + z2;

    x, y = np.meshgrid(x, y)
    return (x, y, z);

def build_gaussian_layer(mean, standard_deviation):
    x = np.arange(-len, len, step);
    y = np.arange(-len, len, step);
    x, y = np.meshgrid(x, y);
    z = np.exp(-((y-mean)**2 + (x - mean)**2)/(2*(standard_deviation**2)))
    z = z/(np.sqrt(2*np.pi)*standard_deviation);
    return (x, y, z);

# 具体函数方法可用 help(function) 查看，如：help(ax.plot_surface)
x1, y1, z1 = build_layer(0.2);
# ax.plot_surface(x1, y1, z1, rstride=1, cstride=1, color='green')

x5, y5, z5 = build_layer(0.15);
# ax.plot_surface(x5, y5, z5, rstride=1, cstride=1, color='pink')

# x2, y2, z2 = build_layer(-0.26);
# ax.plot_surface(x2, y2, z2, rstride=1, cstride=1, color='yellow')
#
# x6, y6, z6 = build_layer(-0.22);
# ax.plot_surface(x6, y6, z6, rstride=1, cstride=1, color='pink')

# x4, y4, z4 = build_layer(0);
# ax.plot_surface(x4, y4, z4, rstride=1, cstride=1, color='purple')

x3, y3, z3 = build_gaussian_layer(0, 1)
ax.plot_surface(x3, y3, z3, rstride=1, cstride=1,cmap='rainbow',alpha=0.8)
plt.show()