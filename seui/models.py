import os.path

from django.db import models
from django import forms


# Create your models here.

class Scores(models.Model):
    """
    绩效分值
    """
    id = models.IntegerField(primary_key=True, name='测试代码', db_column='id')
    item = models.CharField(max_length=255, name='测试名称', db_column='item')
    score = models.FloatField(blank=True, null=True, name='分值', db_column='score')
    multi = models.IntegerField(blank=True, null=True)
    class0 = models.CharField(max_length=255, blank=True, null=True, name='类别', db_column='class0')
    department = models.CharField(max_length=255, blank=True, null=True, name='科室', db_column='department')

    class Meta:
        managed = False
        db_table = 'scores'


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


def uploade_to(instance, filename):
    """
    自定义上传文件位置和文件名
    instance: ModelWithFileField实例
    filename: 上传的文件名
    """
    return os.path.join(instance.appname, filename)


class ModelWithFileField(models.Model):
    """
    useless，用with open方式替代instance.save()/form.save()
    上传文件的模型
    """

    appname = models.CharField(max_length=255, null=True)
    file = models.FileField(upload_to=uploade_to)
    fileorgname = models.CharField(max_length=255)


#  以下是form类

class ScoresForm(forms.ModelForm):
    """
    分值表单
    """

    class Meta:
        model = Scores
        # exclude = ('multi', 'class0', 'department')
        exclude = ('multi',)


# <--以下为上传文件多选相关-->
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ModelFormWithFileField(forms.ModelForm):
    """
    上传文件的模型表单
    useless，可以在前端直接用html写表单,
    HTML: <input type="file" name="upf" >
    request.FILES: <MultiValueDict: {'upf': [<InMemoryUploadedFile: 01a455554c02ba000001bf72ddb34d.jpg (image/jpeg)>]}>
    """

    class Meta:
        model = ModelWithFileField
        fields = ['file']
        # fields = '__all__'
        # exclude = ['fileorgname']
        # 在上面模型的基础上，创建的forms表单添加HTML属性multiple,用于上传多个文件,新版本已废弃.
        # widgets = {
        #     'file': forms.ClearableFileInput(attrs={'multiple': True})
        # }

    # 新版本使用以下类实例实现多文件上传,
    file = MultipleFileField()
# </--以上为上传文件多选相关-->
