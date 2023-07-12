from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '21149109'
API_KEY = 'uTmyaGrGCKTfvA5vKXZgi9lC'
SECRET_KEY = '7fSLtApbCzITyv4YlOvikXqm5RkWavi3'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content('2.png')

""" 调用通用文字识别, 图片参数为本地图片 """
# words_result=client.basicGeneral(image)['words_result']
words_result=client.basicAccurate(image)['words_result']
result=[i['words'] for i in words_result]
print(result)

""" 如果有可选参数 """
options = {}
options["language_type"] = "CHN_ENG"
options["detect_direction"] = "true"
options["detect_language"] = "true"
options["probability"] = "true"

""" 带参数调用通用文字识别, 图片参数为本地图片 """
# words_result=client.basicGeneral(image,options)['words_result']
# result=[i['words'] for i in words_result]
# print(result)

url = "https//www.x.com/sample.jpg"

""" 调用通用文字识别, 图片参数为远程url图片 """
# client.basicGeneralUrl(url)

""" 如果有可选参数 """
options = {}
options["language_type"] = "CHN_ENG"
options["detect_direction"] = "true"
options["detect_language"] = "true"
options["probability"] = "true"

""" 带参数调用通用文字识别, 图片参数为远程url图片 """
# client.basicGeneralUrl(url, options)


import pytesseract
from PIL import Image

image=Image.open(r"C:\Users\Administrator\PycharmProjects\se\baiduai\1.png").convert('L')
image.show()
text=pytesseract.image_to_string(image,lang='chi_sim')
print(text)