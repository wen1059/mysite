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


class AirportNT(models.Model):
    """
    9661老标准新模板
    """
    pri = models.AutoField(primary_key=True, db_column='pri')
    point = models.CharField(max_length=255, blank=True, null=True, db_column='点位')
    n1 = models.IntegerField(db_column='N1', blank=True, null=True)
    n2 = models.IntegerField(db_column='N2', blank=True, null=True)
    n3 = models.IntegerField(db_column='N3', blank=True, null=True)
    n_all = models.IntegerField(db_column='N总', blank=True, null=True)
    lepn_bar = models.FloatField(db_column='Lepn_bar', blank=True, null=True)
    lwecpn = models.FloatField(db_column='Lwecpn', blank=True, null=True)
    record_time = models.DateTimeField(blank=True, null=True, db_column='记录时间')

    class Meta:
        managed = False  # Django不管理此表
        db_table = '机场_9661_新模板'  # 数据库表名


class AirportNew(models.Model):
    # 使用英文命名，通过 db_column 映射到数据库的中文字段
    pri = models.AutoField(primary_key=True, db_column='pri')
    point = models.CharField(max_length=255, blank=True, null=True, db_column='点位')
    date = models.CharField(max_length=255, blank=True, null=True, db_column='日期')
    ldn = models.FloatField(blank=True, null=True, db_column='Ldn')
    nd_effective = models.IntegerField(blank=True, null=True, db_column='Nd_有效')
    nn_effective = models.IntegerField(blank=True, null=True, db_column='Nn_有效')
    nd_all = models.IntegerField(blank=True, null=True, db_column='Nd_总')
    nn_all = models.IntegerField(blank=True, null=True, db_column='Nn_总')
    is_valid = models.BooleanField(blank=True, null=True, db_column='是否有效')
    record_time = models.DateTimeField(blank=True, null=True, db_column='记录时间')

    class Meta:
        managed = False  # Django不管理此表
        db_table = '机场_新标准计算'  # 数据库表名

    def __str__(self):
        return f"{self.point} - {self.date}"


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
