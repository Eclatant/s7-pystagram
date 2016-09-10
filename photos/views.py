from django.shortcuts import render
from django.http import HttpResponse


def hello_world(request):
    return HttpResponse('hello world')


def list_posts(request):
    ctx = {}
    return render(request, 'list.html', ctx)

