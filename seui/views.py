import os.path
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils import timezone
from mysite import settings
from seui.models import *
from django.contrib import messages
from django.views.decorators.gzip import gzip_page
import time
from datetime import datetime
import sys
import shutil
import json
import random


# sys.path.extend([r'C:\Users\Administrator\PycharmProjects\se'])
def get_ip(request):
    """
    获取客户端ip
    X-Forwarded-For:简称XFF头，它代表客户端，也就是HTTP的请求端真实的IP，只有在通过了HTTP 代理或者负载均衡服务器时才会添加该项。
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
    return ip


def upload_file_by_modelform(request, appname):
    """
    上传文件提交按钮
    通过模型表单来上传文件
    appname: 通过调用的app指定appname，写入字段，upload_to函数会读取让文件保存在相应的子目录
    """
    if request.method == 'POST':
        # form = ModelFormWithFileField(request.POST, request.FILES)  # 如果是上传单个文件，加上这行，然后直接form.save()。
        # if form.is_valid():
        for f in (files := request.FILES.getlist('file')):
            # request.FILES: <MultiValueDict: {'file': [<InMemoryUploadedFile: HJ 1048公式.png (image/png)>,... ]
            instance = ModelWithFileField(appname=appname,  # request.POST['title'],
                                          file=f, fileorgname=f.name)
            instance.save()
            # dosomething using f.name
            # os.system(f'start {os.path.join(settings.MEDIA_ROOT, f.name)}')
        return [file.name for file in files]  # 上传的原文件名列表


def index_main(request):
    """
    主域名跳转到指定页面
    """
    return HttpResponseRedirect('/se/sl/')


@gzip_page  # response采用gzip压缩后传到前端
def badapple(request):
    """
    播放字符画视频，
    1、先视频转字符画保存在一个txt，2、读取txt返回json（value为数组）到前端，3、前端js依次读取数组显示。
    """
    if request.method == 'POST':
        if 'frameindex' in request.POST:
            randomlist = ['badapple',
                          '鸡你太美',
                          ]
            with open(os.path.join(settings.STATICFILES_DIRS[0], 'indextext', f'{random.choice(randomlist)}.txt')) as f:
                frametxts = f.read().split('\t')
            # 保存txt到数据库，保存完后注释掉，临时方案，后面重构。太卡放弃。
            # for frame, txt in enumerate(frametxts):
            #     Indextxt(frame=frame, txt=txt).save()
            # idx = int(idx)  # post过来是str
            # txt = Indextxt.objects.get(frame=idx).txt  #  数据库方案，放弃
            # txt = frametxts[idx]
            txt = {'txt': frametxts[40:]}  # 跳过前40帧
            return JsonResponse(txt)  # 改为全部帧传到前端js控制播放
    return render(request, 'se/badapple.html', )


def wpscore(request):
    """
    绩效分值页面
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = ScoresForm()
        data = Scores.objects.order_by('-测试代码')
        content = {'scores': data, 'form': form}
        return render(request, 'se/wpscore.html', content)
    elif request.method == 'POST':
        form = ScoresForm(request.POST)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect('/se/wpscore/')


def wpcal(request):
    """
    绩效计算页面
    """
    if request.method == 'GET':
        datas = Records.objects.filter(appname='绩效分值计算').order_by('-timestamp')
        content = {'datas': datas}
        return render(request, 'se/wpcal.html', content)
    elif request.method == 'POST':
        from se.绩效分值计算 import code_calscore as cocal
        starttime = request.POST['start']
        endtime = request.POST['end']
        siotext: str = cocal.main(starttime, endtime)
        # siotext = '123'
        # time.sleep(2)
        fileout = siotext.split()[-1]
        fileout_f = fileout.split('\\')[-1]
        ip = get_ip(request)
        Records.objects.create(timestamp=timezone.now(), filein=f'{starttime} / {endtime}', fileout=fileout_f,
                               fileout_f=fileout_f, ip=ip, appname='绩效分值计算')
        messages.info(request, siotext)
        return HttpResponseRedirect('/se/wpcal/')


def ptc(request):
    """
    pdf转csv页面
    """
    if request.method == 'GET':
        form = ModelFormWithFileField()
        datas = Records.objects.filter(appname='pdftocsv').order_by('-timestamp')
        content = {'datas': datas, 'form': form}
        # messages.info(request, '12\n34')
        return render(request, 'se/ptc.html', content)
    elif request.method == 'POST':
        # pdf转csv提交按钮
        # 已合并至ptc()，先前作为提交按钮的view函数，现在提交按钮也定位到ptc(), 根据request.method判断。
        from se.single import pdf_to_csv
        files = upload_file_by_modelform(request, appname='pdftocsv')  # 上传文件到media，返回原文件名列表
        pdffiles = [i for i in files if i.lower().endswith('.pdf')]
        for orgname in pdffiles:
            # 上传后文件会被改名，通过原文件名查找上传后的名字，格式为子目录(如果有)+修改后的名字
            # 有重复上传的通过order_by('-id')[0]取最近一次上传，django不支持负索引，通过.file取file字段
            uploadename = ModelWithFileField.objects.filter(fileorgname=orgname).order_by('-id')[0].file.name
            fullname = os.path.join(settings.MEDIA_ROOT, uploadename)  # orgname的绝对路径,用于se程序
            pdf_to_csv.transe(fullname)
            fileout = uploadename.replace(uploadename[-4:], '.csv')  # 子目录+csv文件名，用于media连接
            fileout_f = os.path.split(fileout)[-1]  # csv文件名，用于显示
            ip = get_ip(request)
            Records.objects.create(timestamp=timezone.now(), filein=orgname, fileout=fileout,
                                   fileout_f=fileout_f, ip=ip, appname='pdftocsv')
        content = '\n'.join([i for i in pdffiles]) if pdffiles else '没有要转换的文件'
        messages.info(request, content)
        return HttpResponseRedirect('/se/ptc/')


def ptw(request):
    """
    pdf转word页面
    """
    if request.method == 'GET':
        form = ModelFormWithFileField()
        datas = Records.objects.filter(appname='pdftoword').order_by('-timestamp')
        content = {'datas': datas, 'form': form}
        return render(request, 'se/ptw.html', content)
    elif request.method == 'POST':
        from se.single import pdf_to_word
        files = upload_file_by_modelform(request, appname='pdftoword')  # 上传文件到media，返回原文件名列表
        pdffiles = [i for i in files if i.lower().endswith('.pdf')]
        for orgname in pdffiles:
            # 上传后文件会被改名，通过原文件名查找上传后的名字，格式为子目录(如果有)+修改后的名字
            # 有重复上传的通过order_by('-id')[0]取最近一次上传，django不支持负索引，通过.file取file字段
            uploadename = ModelWithFileField.objects.filter(fileorgname=orgname).order_by('-id')[0].file.name
            fullname = os.path.join(settings.MEDIA_ROOT, uploadename)  # orgname的绝对路径
            pdf_to_word.convert(fullname)
            fileout = uploadename.replace(uploadename[-4:], '.docx')  # 子目录+word文件名，用于media连接
            fileout_f = os.path.split(fileout)[-1]  # word文件名，用于显示
            ip = get_ip(request)
            Records.objects.create(timestamp=timezone.now(), filein=orgname, fileout=fileout,
                                   fileout_f=fileout_f, ip=ip, appname='pdftoword')
        content = '\n'.join([i for i in pdffiles]) if pdffiles else '没有要转换的文件'
        messages.info(request, content)
        return HttpResponseRedirect('/se/ptw/')


def ppr(request):
    """
    移除pdf编辑限制的密码
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = ModelFormWithFileField()
        datas = Records.objects.filter(appname='pdfpasswdremove').order_by('-timestamp')
        content = {'datas': datas, 'form': form}
        return render(request, 'se/ppr.html', content)
    elif request.method == 'POST':
        from se.single import pdfpasswdremover
        files = upload_file_by_modelform(request, appname='pdfpasswdremove')
        pdffiles = [i for i in files if i.lower().endswith('.pdf')]
        for orgname in pdffiles:
            uploadename = ModelWithFileField.objects.filter(fileorgname=orgname).order_by('-id')[0].file.name
            fullname = os.path.join(settings.MEDIA_ROOT, uploadename)  # orgname的绝对路径
            pdfpasswdremover.unlock_cover(fullname)
            fileout = uploadename  # .replace(uploadename[-4:], '_PasswordRemoved.pdf')
            fileout_f = os.path.split(fileout)[-1]
            ip = get_ip(request)
            Records.objects.create(timestamp=timezone.now(), filein=orgname, fileout=fileout,
                                   fileout_f=fileout_f, ip=ip, appname='pdfpasswdremove')
        content = '\n'.join([i for i in pdffiles]) if pdffiles else '没有要转换的文件'
        messages.info(request, content)
        return HttpResponseRedirect('/se/ppr/')


def opr(request):
    """
    移除excel、word编辑限制
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = ModelFormWithFileField()
        datas = Records.objects.filter(appname='officepasswdremove').order_by('-timestamp')
        content = {'datas': datas, 'form': form}
        return render(request, 'se/opr.html', content)
    elif request.method == 'POST':
        from se.single import excel去加密 as epr
        from se.single import word去加密 as wpr
        files = upload_file_by_modelform(request, appname='officepasswdremove')
        xlsfiles = [i for i in files if i.lower().endswith(('.xls', '.xlsx'))]
        docfiles = [i for i in files if i.lower().endswith(('.doc', '.docx'))]
        for orgname in (officefiles := xlsfiles + docfiles):
            uploadename = ModelWithFileField.objects.filter(fileorgname=orgname).order_by('-id')[0].file.name
            fullname = os.path.join(settings.MEDIA_ROOT, uploadename)  # orgname的绝对路径
            if orgname in xlsfiles:
                epr.run(fullname)
            elif orgname in docfiles:
                wpr.run(fullname)
            fileout = uploadename if uploadename.lower().endswith('x') else uploadename + 'x'  # 上传的旧版文件会转为新版
            fileout_f = os.path.split(fileout)[-1]
            ip = get_ip(request)
            Records.objects.create(timestamp=timezone.now(), filein=orgname, fileout=fileout,
                                   fileout_f=fileout_f, ip=ip, appname='officepasswdremove')
        content = '\n'.join([i for i in officefiles]) if officefiles else '没有要转换的文件'
        messages.info(request, content)
        return HttpResponseRedirect('/se/opr/')


def sl(request):
    """
    查询sql，生成lims读取谱图的通用模板
    :param request:
    :return:
    """
    if request.method == 'GET':
        datas = Records.objects.filter(appname='lims查询').order_by('-timestamp')[:30]
        content = {'datas': datas}
        return render(request, 'se/sl.html', content)
    elif request.method == 'POST':
        from se.single import searchlimsql as sls
        testno = request.POST['testno']
        projectno = request.POST['projectno']
        filename = f'{testno}_{projectno}.xlsx'
        rst = sls.searchlims(testno, projectno)
        sls.gentmp(rst, filename)
        ip = get_ip(request)
        Records.objects.create(timestamp=timezone.now(), filein=f'{testno} - {projectno}', fileout=filename,
                               fileout_f=filename, ip=ip, appname='lims查询')
        return HttpResponseRedirect('/se/sl/')


def test(request):
    if request.method == 'GET':
        return render(request, 'se/test.html', {'data': 132})
    elif request.method == 'POST':
        # if 'method' in request.POST:
        #     return HttpResponse('form1')
        upf = request.FILES.get('upload')
        with open(rf"C:\Users\Administrator\Desktop\ftp\{upf}1", 'wb+') as f:
            for chuck in upf.chunks():
                f.write(chuck)
        return HttpResponseRedirect('/se/test/')

