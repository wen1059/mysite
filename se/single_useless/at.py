# -*- coding: utf-8 -*-
# date: 2022/5/20

def out(a):
    def dec(fun):
        print('de')
        def wap(x):
            print(a)
            return fun(x)

        return wap
    return dec


@out('out')
def f(x):
    print('f')
    return x * 2


print(f(6))
