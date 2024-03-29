from glob import glob
import os
import sys


# files  = glob(os.path.join(os.path.split(sys.argv[0])[0], '*.*'))
# for file in files:
#     print(file)

def a(*color):
    a, *b = color
    print(a)
    print(b)

a(1,2,3)
