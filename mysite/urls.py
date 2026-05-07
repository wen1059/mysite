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
from django.http import HttpResponse
from django.views.generic.base import RedirectView

urlpatterns = [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    # path('admin/', admin.site.urls),
    # path('favicon.ico', RedirectView.as_view(url='https://10.1.224.117/static/img/Hornet_Idle.png')),

    path('', views.index_main),
    path('test/', views.test),
    path('test/api/', views.test_api),
    path('badapple/', views.badapple),
    path('badapple/api/', views.badapple_api),
    path('showcode/', views.showcode),
    path('uph/', views.uploadhandle),
    path('ap/', views.airport),  # 机场噪声查询
    path('sp/', views.sp),  # 采样准备
    path('sp/api/', views.sp_api),  # 采样准备表格api

]
