import threading,multiprocessing,time,cv2
def funca(a,b):
    for i in range(b):
        a+=1
    print(a)
    return a
def funcb(a,b):
    for i in range(b):
        a-=1.01
    print(a)
    return a
def funcc(a,b):
    for i in range(b):
        a+=1.02
    print(a)
    return a
funcs=[funca,funcb,funcc]
a,b=1,50000000

def srun():
    print(time.ctime())
    funca(a,b)
    funcb(a, b)
    funcc(a, b)
    funcc(a, b)
    print(time.ctime()+'\n')
def trun():
    t1 = threading.Thread(target=funcs[0], args=(a, b))
    t2 = threading.Thread(target=funcs[1], args=(a, b))
    t3 = threading.Thread(target=funcs[2], args=(a, b))
    t4 = threading.Thread(target=funcs[2], args=(a, b))
    threds = [t1, t2, t3,t4]
    print(time.ctime())
    for t in threds:
        t.start()
    for t in threds:
        t.join()
    print(time.ctime()+'\n')
def mrun():
    t1 = multiprocessing.Process(target=funcs[0], args=(a, b))
    t2 = multiprocessing.Process(target=funcs[1], args=(a, b))
    t3 = multiprocessing.Process(target=funcs[2], args=(a, b))
    t4 = multiprocessing.Process(target=funcs[2], args=(a, b))
    threds = [t1, t2, t3,t4]
    print(time.ctime())
    for t in threds:
        t.start()
    for t in threds:
        t.join()
    print(time.ctime()+'\n')
# if __name__=='__main__':
#     srun()
#     trun()
#     mrun()

if __name__=='__main__':
    cap=cv2.VideoCapture('single.jpg')
    def captest(cap):
        print(cap)
    # t1=threading.Thread(target=captest,args=(cap,))
    # t2= threading.Thread(target=captest, args=(cap,))
    # t1.start()
    # t2.start()
    p1=multiprocessing.Process(target=captest,args=(cap,))
    p2 = multiprocessing.Process(target=captest, args=(cap,))
    p1.start()
    p2.start()