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
    useless,用简单文件上传取代
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
                          # '鸡你太美',
                          ]
            with open(os.path.join(settings.STATICFILES_DIRS[0], 'indextext', f'{random.choice(randomlist)}.txt')) as f:
                frametxts = f.read().split('\t')
            txt = {'txt': frametxts[40:]}  # 跳过前40帧
            return JsonResponse(txt)  # 改为全部帧传到前端js控制播放
    return render(request, 'se/badapple.html', {'appname': 'badapple'})


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


class UploadHandle:
    """
    文件上传后处理并返回新文件，这些网页的类。
    """

    def __init__(self, appname):
        self.appname = appname  # appname，文件上传到media下的子目录名/数据库appname字段
        self.sql_datas = Records.objects.filter(appname=self.appname).order_by('-timestamp')  # 数据库data
        self.content = {'datas': self.sql_datas, 'appname': self.appname}  # render到前端的数据
        self.destination = ''  # 上传文件的绝对路径，会由后续函数更新
        self.new_ext = ''  # 处理后新文件的扩展名，为了重命名fileout，会由后续函数更新

    def uploadfile(self, request):
        """
        简单文件上传，通过with open保存。
        <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <input type="file" name="upf" >
        <input type="submit">
        </form>
        :param basedir: 保存到的子目录（appname）
        :param request:
        :return:
        """
        assert request.method == 'POST'
        upf = request.FILES.get('upf')
        with open(destination := os.path.join(settings.MEDIA_ROOT, self.appname, upf.name), 'wb+') as f:
            for chuck in upf.chunks():
                f.write(chuck)
        self.destination = destination

    def ptc_handle(self, request):
        """
        处理上传的文件
        :param request:
        :return:
        """
        from se.single import pdf_to_csv
        pdf_to_csv.transe(self.destination)
        self.new_ext = '.csv'

    def ptw_handle(self, request):
        from se.single import pdf_to_word
        pdf_to_word.convert(self.destination)
        self.new_ext = '.docx'

    def ppr_handle(self, request):
        from se.single import pdfpasswdremover
        pdfpasswdremover.unlock_cover(self.destination)
        self.new_ext = '.pdf'

    def opr_handle(self, request):
        from se.single import excel去加密 as epr
        from se.single import word去加密 as wpr
        if self.destination.lower().endswith(('.xls', '.xlsx')):
            epr.run(self.destination)
            self.new_ext = '.xlsx'
        elif self.destination.lower().endswith(('.doc', '.docx')):
            wpr.run(self.destination)
            self.new_ext = '.docx'

    def create_records(self, request):
        Records.objects.create(timestamp=timezone.now(),
                               filein=(filein := os.path.split(self.destination)[-1]),
                               fileout=filein.split('.')[0] + self.new_ext,
                               ip=get_ip(request),
                               appname=self.appname
                               )


def ptc(request):
    """
    pdf转csv页面
    """
    handle = UploadHandle('pdftocsv')
    if request.method == 'GET':
        return render(request, 'se/base_upload.html', handle.content)
    elif request.method == 'POST':
        # pdf转csv提交按钮
        # 已合并至ptc()，先前作为提交按钮的view函数，现在提交按钮也定位到ptc(), 根据request.method判断。
        handle.uploadfile(request)
        handle.ptc_handle(request)
        handle.create_records(request)
        # content = '\n'.join([i for i in pdffiles]) if pdffiles else '没有要转换的文件'
        # messages.info(request, content)
        return HttpResponseRedirect('/se/ptc/')


def ptw(request):
    """
    pdf转word页面
    """
    handle = UploadHandle('pdftoword')
    if request.method == 'GET':
        return render(request, 'se/base_upload.html', handle.content)
    elif request.method == 'POST':
        handle.uploadfile(request)
        handle.ptw_handle(request)
        handle.create_records(request)
        return HttpResponseRedirect('/se/ptw/')


def ppr(request):
    """
    移除pdf编辑限制的密码
    :param request:
    :return:
    """
    handle = UploadHandle('pdfpasswdremove')
    if request.method == 'GET':
        return render(request, 'se/base_upload.html', handle.content)
    elif request.method == 'POST':
        handle.uploadfile(request)
        handle.ppr_handle(request)
        handle.create_records(request)
        return HttpResponseRedirect('/se/ppr/')


def opr(request):
    """
    移除excel、word编辑限制
    :param request:
    :return:
    """
    handle = UploadHandle('officepasswdremove')
    if request.method == 'GET':
        return render(request, 'se/base_upload.html', handle.content)
    elif request.method == 'POST':
        handle.uploadfile(request)
        handle.opr_handle(request)
        handle.create_records(request)
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
        return render(request, 'se/test.html')
    elif request.method == 'POST':
        # print(request.POST, request.FILES)
        # upload_file(request, 'test')
        return HttpResponseRedirect('/se/test/')
