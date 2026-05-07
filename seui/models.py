import os.path

from django.db import models
from django import forms


# Create your models here.


class Airport(models.Model):
    """
    机场噪声
    """
    pri = models.AutoField(db_column='pri', primary_key=True)
    position = models.CharField(db_column='点位', max_length=255, blank=True, null=True)  # 点位
    acq_date = models.CharField(db_column='日期', max_length=255, blank=True, null=True)  # 日期
    analylize = models.CharField(db_column='分析员', max_length=255, blank=True, null=True)  # 分析员
    n1 = models.IntegerField(db_column='N1', blank=True, null=True)
    n2 = models.IntegerField(db_column='N2', blank=True, null=True)
    n3 = models.IntegerField(db_column='N3', blank=True, null=True)
    nall = models.IntegerField(db_column='N总', blank=True, null=True)
    lamaxpb = models.FloatField(db_column='Lamaxpb', blank=True, null=True)
    lwecpn = models.FloatField(db_column='Lwecpn', blank=True, null=True)
    n1_20 = models.IntegerField(db_column='N1_20', blank=True, null=True)
    n2_20 = models.IntegerField(db_column='N2_20', blank=True, null=True)
    n3_20 = models.IntegerField(db_column='N3_20', blank=True, null=True)
    nall_20 = models.IntegerField(db_column='N总_20', blank=True, null=True)
    lamaxpb_20 = models.FloatField(db_column='Lamaxpb_20', blank=True, null=True)
    lwecpn_20 = models.FloatField(db_column='Lwecpn_20', blank=True, null=True)
    bg = models.FloatField(db_column='背景', blank=True, null=True)  # 背景
    cal_date = models.DateTimeField(db_column='记录时间', blank=True, null=True)  # 记录时间

    class Meta:
        managed = False
        db_table = '机场_day_精密_2023'


class Records(models.Model):
    """
    操作记录
    """
    id = models.AutoField(primary_key=True)
    filein = models.CharField(max_length=255, null=True)
    fileout = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(null=True)
    ip = models.GenericIPAddressField(null=True)
    appname = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ('-timestamp',)
