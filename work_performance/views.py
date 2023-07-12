from django.shortcuts import render

# Create your views here.

from work_performance.models import *
from django.http import HttpResponseRedirect


def index(request):
    form = ScoresForm()
    data = Scores.objects.order_by('-测试代码')
    content = {'scores': data, 'form': form}
    return render(request, 'wp/wp.html', content)


def addscore(request):
    if request.method == 'POST':
        form = ScoresForm(request.POST)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect('/wp')
