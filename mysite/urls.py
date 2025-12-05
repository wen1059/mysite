"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from seui import views
from mysite import settings
from django.views.static import serve

urlpatterns = [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    # path('admin/', admin.site.urls),

    path('', views.index_main),
    # path('se/', include('seui.urls', namespace='seui')),
    path('se/test/', views.test, name='test'),
    path('se/badapple/', views.badapple, name='badapple'),
    # path('wpscore/', views.wpscore, name='wpscore'),  # 绩效分值
    # path('wpcal/', views.wpcal, name='wpcal'),  # 绩效计算
    path('se/uph/', views.uploadhandle, name='uploadhandle'),
    # path('sl/', views.sl, name='sl'),  # 生成lims谱图通用模板
    # path('dp/', views.drawpic, name='dp'),  # 绘制渐变图
    path('se/ap/', views.airport, name='ap'),  # 机场噪声查询
    path('se/sp/', views.sp, name='sp'),  # 采样准备
    path('se/sp/api/', views.sp_api, name='sp'),  # 采样准备表格api

]
