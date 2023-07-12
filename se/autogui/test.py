import pyautogui
from PIL import Image,ImageGrab
im=ImageGrab.grab(bbox=())
# im.show()
im.save('te.png')
loca=pyautogui.locateOnScreen('te.png')
print(loca)

import pytesseract
text=pytesseract.image_to_string('te.png',lang='chi_sim')
print('*'+'\n'+text)