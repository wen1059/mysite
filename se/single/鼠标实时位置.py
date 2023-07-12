import pyautogui
while True:
    x,y=pyautogui.position()
    posstr=str(x).rjust(4)+' '+str(y).rjust(4)
    print(posstr,end='')
    print('\b'*len(posstr),end='',flush=True)
