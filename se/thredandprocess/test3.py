from concurrent.futures import ProcessPoolExecutor,as_completed
import time
import random


def fun(b):
    a=1
    for i in range(1,80000):
       a*=i
    # print(a)
    return b

# print(time.ctime())
# for i in range(16):
#     print(fun(i))
# print(time.ctime())
if __name__ == '__main__':
    l = []
    print(time.ctime())
    with ProcessPoolExecutor() as exec:

        pool=[exec.submit(fun,n) for n in range(16)]
        for i in as_completed(pool):
            # print(i.result())
            l.append(i.result())
            pass
        # print(exlist)

    print(time.ctime())
    print(l)

