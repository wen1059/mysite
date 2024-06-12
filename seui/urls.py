# -*- coding: utf-8 -*-
# date: 2022-9-7
from django.urls import path
from seui import views

app_name = 'seui'
urlpatterns = [
    path('test/', views.test, name='test'),
    path('badapple/', views.badapple, name='badapple'),
    path('wpscore/', views.wpscore, name='wpscore'),  # 绩效分值
    path('wpcal/', views.wpcal, name='wpcal'),  # 绩效计算
    path('ptc/', views.ptc, name='ptc'),  # pdf转csv
    path('ptw/', views.ptw, name='ptw'),  # pdf转word
    path('ppr/', views.ppr, name='ppr'),  # pdf移除密码
    path('opr/', views.opr, name='opr'),  # excel、word移除密码
    path('sl/', views.sl, name='sl'),  # 生成lims谱图通用模板
    path('dp/', views.drawpic, name='dp'),  # 绘制渐变图
    path('ap/', views.airport, name='ap'),  # 机场噪声查询

]
