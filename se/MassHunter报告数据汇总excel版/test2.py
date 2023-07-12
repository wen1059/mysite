# class A():
#     def __init__(self):
#         self.name='a'
#     def fun(self):
#         return self.name
# import changetolims
# import xlwings
# def foo():
#     print('in the foo')
#
#     def bar():
#         print('in the bar')
#
#     bar()
# foo()
a=list(range(10).__reversed__())
a[0]=a[0].__add__(1)
print(a)