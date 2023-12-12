# -*- coding: utf-8 -*-
# date: 2022-9-7
from django.urls import path
from seui.views import *

app_name = 'seui'
urlpatterns = [
    path('', badapple, name='index_se'),
    path('wpscore/', wpscore, name='wpscore'),  # 绩效分值
    path('wpcal/', wpcal, name='wpcal'),  # 绩效计算
    path('ptc/', ptc, name='ptc'),  # pdf转csv
    path('ptw/', ptw, name='ptw'),  # pdf转word
    path('ppr/', ppr, name='ppr'),  # pdf移除密码
    path('opr/', opr, name='opr'),  # excel、word移除密码
    path('sl/', sl, name='sl'),  # 生成lims谱图通用模板

]
