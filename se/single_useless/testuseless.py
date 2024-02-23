import os

instrumentname = os.path.split(os.path.realpath(__file__))[1].replace('.py', '')
print(instrumentname)
