from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.gzip import gzip_page
from mysite import settings
from seui.models import *

import csv
import os.path
from datetime import datetime, timedelta
import sys
import random
import string

sys.path.append(r'C:\Users\Administrator\PycharmProjects\se')


def get_ip(request):
    """
    获取客户端ip
    X-Forwarded-For:简称XFF头，它代表客户端，也就是HTTP的请求端真实的IP，只有在通过了HTTP 代理或者负载均衡服务器时才会添加该项。
    """
    return xf if (xf := request.META.get('HTTP_X_FORWARDED_FOR')) else request.META.get('REMOTE_ADDR')


def printip(func):
    """
    装饰器，打印访问者ip
    :param func:
    :return:
    """

    def inner(request):
        print(get_ip(request), request.path)
        return func(request)

    return inner


def simple_upload_file(request):
    """
    简单文件上传。with open方式保存
    :param request:
    :return:
    """
    if request.method == 'POST':
        # 获取前端表单<input type="file">标签传过来的name属性.可以直接赋值，此处为了适应前端不同的name值。
        key = list(request.FILES.keys())[0]
        files = request.FILES.getlist(key)
        for file in files:
            # 限制上传文件大小100mb
            if file.size > 100 * 1024 * 1024:
                continue
            # savefile
            with open(destination := os.path.join(settings.MEDIA_ROOT, file.name), 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
                yield destination


def index_main(request):
    """
    主域名跳转到指定页面
    """
    return HttpResponseRedirect('/showcode/')


def showcode(request):
    with open(r"C:\Users\Administrator\PycharmProjects\se\single\send_file_to_yunce.py", encoding='utf8') as f:
        code = f.read()
    return render(request, 'showcode.html', {'code': code})


@printip
def badapple(request):
    """
    播放字符画视频，
    1、先视频转字符画保存在一个txt，2、读取txt返回json（value为数组）到前端，3、前端js依次读取数组显示。
    """
    return render(request, 'badapple.html')


@gzip_page  # response采用gzip压缩后传到前端
def badapple_api(request):
    randomlist = [
        'badapple.txt',
        # '鸡你太美.txt',
    ]
    with open(os.path.join(settings.STATICFILES_DIRS[0], 'indextext', random.choice(randomlist))) as f:
        # 用随机字母显示
        frametxts = f.read().replace('R', random.choice(string.ascii_uppercase)).split('\t')
    txts = {'txts': frametxts[40:]}  # 跳过前40帧
    return JsonResponse(txts)  # 改为全部帧传到前端js控制播放


def uploadhandle(request):
    """
    文件上传后处理并返回新文件，这些网页的视图。
    :param request:
    :return:
    """
    if request.method == 'POST':
        mode = request.POST.get('mode')
        for destination in simple_upload_file(request):
            # dosomethingwithfile
            match mode:
                case 'ptc':
                    from single import pdf_to_csv
                    outputname = pdf_to_csv.transe(destination)
                case 'ptw':
                    from single import pdf_to_word
                    outputname = pdf_to_word.convert(destination)
                case 'ppr':
                    from single import pdfpasswdremover
                    outputname = pdfpasswdremover.unlock(destination)
                case 'epr':
                    from single import excel去加密 as epr
                    outputname = epr.run(destination)
                case 'wpr':
                    from single import word去加密 as wpr
                    outputname = wpr.run(destination)
                case _:
                    outputname = 'unknown'

            # createrecord
            Records.objects.create(
                filein=destination.split('\\')[-1],
                fileout=outputname,
                timestamp=timezone.now(),
                ip=get_ip(request),
                appname=mode
            )
        return HttpResponseRedirect('/uph/')

    queryset = Records.objects.order_by('-timestamp')
    return render(request, 'uploadhandle.html', {'datas': queryset})


def airport(request):
    """
    机场噪声结果查询界面
    :param request:
    :return:
    """
    if 'cleartab' in request.POST:  # 清空数据库
        Airport.objects.all().delete()
    if 'checkformatting' in request.POST:  # 检查格式
        from 机场噪声_2021虹桥 import 检查格式_RE as ck
        table = ck.showcheckresult(r"\\10.1.78.254\环装-实验室\实验室共享\2024鸡场\__检查格式__")
        return HttpResponse(table)
    queryset = Airport.objects.order_by('-cal_date')
    return render(request, 'airport.html', {'queryset': queryset})


@printip
def sp(request):
    return render(request, 'sp.html')


def sp_api(request):
    from single import yunce_SamplingPreparation as ycsp
    result = ycsp.getjson()
    return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})


def test(request):
    return render(request, 'sp.html')


def test_api(request):
    from ...se.single import yunce_SamplingPreparation as ycsp
    result = ycsp.getjson()
    return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})
