# -*- coding: utf-8 -*-
# date: 2022-11-22
"""
吾爱破解开源代码
"""
import requests
from lxml import etree
import os
import time
import json


def Get_ID_Name(url, headers):
    Contents_IDS = []
    r = requests.get(url, headers=headers)
    print(r)
    r.encoding = r.apparent_encoding
    html = etree.HTML(r.text)
    Titles = html.xpath('//*[@id="award"]/main/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/h1')
    Contents_lists = html.xpath('//*[@id="anchor_sound_list"]/div[2]/ul/li/div[2]/a/span/text()')
    for Contents_list in Contents_lists:
        links_Cache = str(Contents_list).split('/')[-1]
        JsonURL = 'https://www.ximalaya.com/revision/play/v1/audio?id={}&ptype=1'.format(links_Cache)
        Contents_IDS.append(JsonURL)
    return Titles, Contents_IDS


def Json_Get_links(Contents_IDS, headers):
    Itemlists = []
    n = 0
    for Contents_ID in Contents_IDS:
        contents = {}
        time.sleep(1.5)
        r1 = requests.get(Contents_ID, headers=headers)
        r1.encoding = r1.apparent_encoding
        results = json.loads(r1.text)
        id = results['transdata']['trackId']
        m4alinks = results['transdata']['src']
        contents['ID'] = id
        contents['M4aLinks'] = m4alinks
        Itemlists.append(contents)
        n += 1
        print('已采集{}个链接！'.format(n))
    # print(Itemlists)
    return Itemlists


def DownLoadM4A(Itemlists, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4208.400',
        # 'If-None-Match': '"llN9ISnSdOkEmb835lC9NQ_j47Kl"',
        # 'Host': 'fdfs.xmcdn.com',
    }
    if not os.path.exists('./XMLYFM'):
        os.mkdir('./XMLYFM')
    count = 0
    for filename1, Itemlist in zip(filename, Itemlists):
        srclinks = Itemlist['M4aLinks']
        print(srclinks)
        r2 = requests.get(srclinks, headers=headers)
        print(r2)
        # print(r2.raise_for_status())
        with open('./XMLYFM/' + str(filename1) + '.m4a', 'wb') as f:
            f.write(r2.content)
            count += 1
            print('已下载{}个音频文件！'.format(count))
    print("{}个音频文件已全部下载完成！".format(count))


if __name__ == '__main__':
    print('正在加载...')
    url = 'https://www.ximalaya.com/album/31329891'  # 更换URL下载页面内所有链接
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4208.400',
        'Cookie': '_xmLog=h5&a81f9167-2af8-47a1-a1cf-ce6132beb6fa&process.env.sdkVersion; xm-page-viewid=ximalaya-web; x_xmly_traffic=utm_source%3A%26utm_medium%3A%26utm_campaign%3A%26utm_content%3A%26utm_term%3A%26utm_from%3A; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1668995409,1669083556; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1669083779',
        # 'Referer': 'https://www.ximalaya.com/gerenchengzhang/29391994/',
        # 'Host': 'www.ximalaya.com'
    }
    data1 = Get_ID_Name(url, headers)
    IDlinks = data1[1]
    fileName = data1[0]
    DownLoadM4A(Json_Get_links(IDlinks, headers), fileName)
