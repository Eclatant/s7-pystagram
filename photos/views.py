from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from .models import Post, Comment

def hello_world(request):
    return HttpResponse('hello world')

def list_posts(request):
    page = request.GET.get('page', 1)
    per_page = 2

    posts = Post.objects.all().order_by('-created_at')
    pgt = Paginator(posts, per_page)
    try:
        contents = pgt.page(page)
    except PageNotAnInteger:
        contents = pgt.page(1)
    except EmptyPage:
        contents = []

    ctx = {
        'posts' : contents,
    }
    return render(request, 'list.html', ctx)

"""def list_posts(request):
    per_page = 2
    try:
        page = request.GET.get('page', '')
        if page.isdigit():
            page = int(page)
        if page < 1:
            page = 1
    except(TypeError, ValueError):
        page = 1

    posts = Post.objects.all().order_by('-created_at')
    ctx = {
        'posts' : posts[(page-1)*per_page:page*per_page],
    }
    return render(request, 'list.html', ctx)
"""

def view_post(request, pk):
    #post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    ctx = { 'post': post }
    return render(request, 'view.html', ctx)

def create_post(request):
    ctx = {}
    if request.method == 'POST':
        form = request.POST
        content = form['content']
        post = Post()
        post.content = content
        post.save()
        #url = reverse('photos:view_post', kwargs={'pk':post.pk})
        #return redirect(url)
        return redirect('photos:view_post', pk=post.pk)
    return render(request, 'edit.html', ctx)

def delete_comment(request, pk, post_pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = get_object_or_404(Post, pk=post_pk)
    ctx = {'comment': comment }
    if request.method == 'POST':
        comment.delete()
        return redirect('photos:view_post', pk=post.pk)
    return render(request, 'delete_comment.html', ctx)

def create_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = request.POST
        content = form['content']
        comment = Comment()
        comment.post = post
        comment.content = content
        comment.save()
        return redirect('photos:view_post', pk=post.pk)
    return render(request, 'create_comment.html')
