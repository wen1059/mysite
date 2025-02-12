"""
下载一元简史音频
fiddler抓包桌面微信小程序
地址  /interfaces//api/eduCourseKpoint/list   获得json里面有m4a下载地址。
"""

import json
import os
from glob import glob
import requests

path = r"C:\Users\Administrator\Downloads\闲话南北朝天下归一"
num = 0
for file in glob(f'{path}\\*.json'):
    with open(file, encoding='utf-8') as f:
        data = f.read()
        data = json.loads(data, strict=False)
        for list_ in data['data']['list']:
            name = list_['audioInfo']['name']
            url = list_['audioInfo']['url']
            print(name,url)
            response = requests.get(rf'http://file.yiyuanjianshi.com/{url}')
            with open(os.path.join(path, f'{num}、{name}.m4a'), 'wb') as downloadfile:
                downloadfile.write(response.content)
                num += 1
