from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .models import Post


def hello_world(request):
    return HttpResponse('hello world')


def list_posts(request):
    per_page = 2
    try:
        page = request.GET.get('page', '')
        if page.isdigit():
            page = int(page)
        if page < 1:
            page = 1
    except (TypeError, ValueError):
        page = 1

    posts = Post.objects.all().order_by('-created_at')

    ctx = {
        'posts': posts[(page-1)*per_page:page*per_page],
    }
    return render(request, 'list.html', ctx)


def view_post(request, pk):
    #post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    ctx = {}
    return render(request, 'view.html', ctx)


def create_post(request):
    ctx = {}
    return render(request, 'edit.html', ctx)


