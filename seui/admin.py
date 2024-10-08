from django.contrib import admin

# Register your models here.
from seui.models import *


class ScoresAdmin(admin.ModelAdmin):
    # pass
    list_display = ('测试代码', '测试名称', '分值')


class AirportAdmin(admin.ModelAdmin):
    list_display = ['pri']


admin.site.register(Scores, ScoresAdmin)
admin.site.register(Records)
admin.site.register(ModelWithFileField)
admin.site.register(Airport, AirportAdmin)
