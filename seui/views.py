import csv
import os.path
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils import timezone
from mysite import settings
from seui.models import *
from django.contrib import messages
from django.views.decorators.gzip import gzip_page
import time
from datetime import datetime, timedelta
import sys
import shutil
import json
import random

sys.path.append(r'C:\Users\Administrator\PycharmProjects')


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


def simple_upload_file(request):
    """
    简单文件上传。with open方式保存
    :param request:
    :return:
    """
    destinations = []
    if request.method == 'POST':
        # 获取前端表单<input type="file">标签传过来的name属性.可以直接赋值，此处为了适应前端不同的name值。
        key = list(request.FILES.keys())[0]
        files = request.FILES.getlist(key)
        for file in files:
            # 限制上传文件大小100mb
            if file.size > 100 * 1024 * 1024:
                break
            # savefile
            with open(destination := os.path.join(settings.MEDIA_ROOT, file.name), 'wb+') as f:
                for chuck in file.chunks():
                    f.write(chuck)
                destinations.append(destination)
    return destinations


def index_main(request):
    """
    主域名跳转到指定页面
    """
    return HttpResponseRedirect('/se/badapple/')


@gzip_page  # response采用gzip压缩后传到前端
def badapple(request):
    """
    播放字符画视频，
    1、先视频转字符画保存在一个txt，2、读取txt返回json（value为数组）到前端，3、前端js依次读取数组显示。
    """
    if request.method == 'POST':
        if 'frameindex' in (body := json.loads(request.body)):
            randomlist = [
                'badapple',
                '鸡你太美',
            ]
            with open(os.path.join(settings.STATICFILES_DIRS[0], 'indextext', f'{random.choice(randomlist)}.txt')) as f:
                frametxts = f.read().split('\t')
            txts = {'txts': frametxts[40:]}  # 跳过前40帧
            return JsonResponse(txts)  # 改为全部帧传到前端js控制播放
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
                    from se.single import pdf_to_csv
                    outputname = pdf_to_csv.transe(destination)
                case 'ptw':
                    from se.single import pdf_to_word
                    outputname = pdf_to_word.convert(destination)
                case 'ppr':
                    from se.single import pdfpasswdremover
                    outputname = pdfpasswdremover.unlock(destination)
                case 'epr':
                    from se.single import excel去加密 as epr
                    outputname = epr.run(destination)
                case 'wpr':
                    from se.single import word去加密 as wpr
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
        return HttpResponseRedirect('/se/uph/')

    queryset = Records.objects.all().order_by('-timestamp')
    context = {'datas': queryset, 'navname': 'uploadhandle'}
    return render(request, 'se/uploadhandle.html', context)


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


def drawpic(request):
    """
    绘制渐变图
    :param request:
    :return:
    """
    if request.method == 'POST':
        from ...se.single.drawgradient import DrawGradient
        from io import BytesIO
        import base64
        dg = DrawGradient()
        # lamba：16进制颜色转rgb
        dg.basecolor = (lambda x: (int(x[1:3], 16), int(x[3:5], 16), int(x[5:], 16)))(request.POST['selectedcolor'])
        dg.drawpic()
        buffer = BytesIO()
        dg.im.save(buffer, 'png')
        buffer.seek(0)
        return render(request, 'se/drawpic.html',
                      {'img': base64.encodebytes(buffer.read()).decode(), 'appname': 'drawpic'})
    return render(request, 'se/drawpic.html', {'appname': 'drawpic'})


def airport(request):
    """
    机场噪声结果查询界面
    :param request:
    :return:
    """
    if 'cleartab' in request.POST:  # 清空数据库
        Airport.objects.all().delete()

    if pri := request.GET.get('del'):  # 删除某一行
        Airport.objects.filter(pri=pri).delete()

    queryset = Airport.objects.all().order_by('-cal_date')
    # 按条件筛选
    if position := request.GET.get('position'):
        queryset = queryset.filter(position__contains=position)
    if acq_date := request.GET.get('acq_date'):
        queryset = queryset.filter(acq_date__contains=acq_date)
    if cal_date := request.GET.get('cal_date'):
        queryset = queryset.filter(cal_date__range=[cal_date, (
                datetime.strptime(cal_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')])

    if 'export' in request.GET:  # 导出csv
        response = HttpResponse(content_type='text/csv;charset=gbk',
                                headers={"Content-Disposition": 'attachment; filename="export.csv"'},
                                )
        writer = csv.writer(response)
        writer.writerow(
            ['pri', '点位', '日期', '分析员', 'n1', 'n2', 'n3', 'n总', 'lepnb', 'lwecpn', '背景', '记录时间'])
        writer.writerows(queryset.values_list())
        return response
    if 'checkformatting' in request.POST:  # 检查格式
        from se.机场噪声_2021虹桥 import 检查格式_RE as ck
        table = ck.showcheckresult(r"\\10.1.78.254\环装-实验室\实验室共享\2024鸡场\__检查格式__")
        return HttpResponse(table)
    return render(request, 'se/airport.html', {'queryset': queryset, 'appname': 'airport'})


def sp(request):
    return render(request, 'se/sp.html', {'appname': 'sp'})


def sp_api(request):
    from se.single import yunce_SamplingPreparation as ycsp
    jsonresult = ycsp.getjson()
    return JsonResponse(jsonresult, safe=False, json_dumps_params={'ensure_ascii': False})


def test(request):
    return HttpResponse('1')
