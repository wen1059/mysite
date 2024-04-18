import time
def test(request):
    print(time.time())
    randomlist = ['badapple',
                  # '鸡你太美',
                  ]
    with open(r'C:\Users\Administrator\PycharmProjects\mysite\static\indextext\badapple.txt') as f:
        frametxts = f.read().split('\t')
    txt = {'txt': frametxts[40:]}  # 跳过前40帧
    print(time.time())
    return txt  # 改为全部帧传到前端js控制播放

test(1)