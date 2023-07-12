from collections import defaultdict

tree = lambda: defaultdict(tree)

def tree2():
    return defaultdict(tree2)

dd = tree()

dd['a'] = 1
dd['b'] = 2
dd['c']['d'] = 3
dd['e'] = 4
dd[1][2][3] = 5



def listitem(dd):
    for i, j in dd.items():
        if isinstance(j, defaultdict):
            listitem(j)
        else:
            print(i, j)
