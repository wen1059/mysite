import threading,multiprocessing,time,cv2

def gen(val,di):
    l=''
    for i in range(val):
        l+='{}'.format(i)
    di.setdefault('l{}'.format(val),l)


# if __name__=='__main__':
    di = multiprocessing.Manager().dict()
    prs = []
    for i in range(10):
        p = multiprocessing.Process(target=gen, args=(i,di))
        # p = threading.Thread(target=gen, args=(i,))
        prs.append(p)
    for p in prs:
        p.start()
    for p in prs:
        p.join()
    print(di)

if __name__=='__main__':
    lf=[i for i in range(100)]
    print(lf)
    for first in range(16):
        nlf=lf[first::16]
        print(nlf)