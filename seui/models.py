import os.path

from django.db import models
from django import forms


# Create your models here.
# 太卡，磁盘读取严重，放弃
# class Indextxt(models.Model):
#     id = models.AutoField(primary_key=True)
#     frame = models.IntegerField()
#     txt = models.TextField(null=True)


class Records(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(null=True)
    filein = models.CharField(max_length=255, null=True)
    fileout = models.CharField(max_length=255, null=True)
    fileout_f = models.CharField(max_length=255, null=True)
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
    上传文件的模型
    """

    appname = models.CharField(max_length=255, null=True)
    file = models.FileField(upload_to=uploade_to)
    fileorgname = models.CharField(max_length=255)


#  以下是form类
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
    非必要，可以在前端直接用html写表单
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
