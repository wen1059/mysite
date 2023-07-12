# -*- coding: utf-8 -*-
# date: 2022-9-7
from django.urls import path
from work_performance.views import *

app_name = 'work_performance'
urlpatterns = [
    path('', index, name='index'),
    path('add/', addscore,)

]
