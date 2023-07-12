from django.db import models
from django import forms


# Create your models here.
class Scores(models.Model):
    id = models.IntegerField(primary_key=True, name='测试代码', db_column='id')
    item = models.CharField(max_length=255, name='测试名称', db_column='item')
    score = models.FloatField(blank=True, null=True, name='分值', db_column='score')
    multi = models.IntegerField(blank=True, null=True)
    class0 = models.CharField(max_length=255, blank=True, null=True, name='类别', db_column='class0')
    department = models.CharField(max_length=255, blank=True, null=True, name='科室', db_column='department')

    class Meta:
        managed = False
        db_table = 'scores'


class ScoresForm(forms.ModelForm):
    class Meta:
        model = Scores
        # exclude = ('multi', 'class0', 'department')
        exclude = ('multi',)
