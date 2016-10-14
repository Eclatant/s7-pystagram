import logging

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.conf import settings

from .models import Post, Comment, Like
from .forms import PostSimpleForm
from .forms import PostForm
from pystagram.sample_exceptions import HelloWorldError

logger = logging.getLogger(__name__)

def hello_world(request):
    return HttpResponse('hello world')

def list_posts(request):
    user = request.user
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
        'user' : user
    }
    return render(request, 'list.html', ctx)

def view_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    likes = post.like_set.all
    ctx = {
        'post': post,
        'likes': likes
    }
    return render(request, 'view.html', ctx)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) # 위의 세줄을 한줄로
            post.user = request.user
            post.user_name = str(post.user)
            post.save()
            return redirect('photos:view_post', pk=post.pk)
    elif request.method == 'GET':
        form = PostForm()

    ctx = {
        'form': form,
    }

    return render(request, 'edit.html', ctx)

@login_required
def delete_comment(request, pk, post_pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = get_object_or_404(Post, pk=post_pk)
    ctx = {'comment': comment }
    if request.method == 'POST':
        comment.delete()
        return redirect('photos:view_post', pk=post.pk)
    return render(request, 'delete_comment.html', ctx)

@login_required
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

@login_required
def add_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    qs = post.like_set.filter(user=request.user)
    did_like = qs.exists()
    result_txt = ''

    ctx = {
        'post': post,
        'did_like': did_like
        }

    if did_like:
        qs.delete()
    else:
        qs.create(post=post, user=request.user)

    return render(request, 'like_result.html', ctx)

def user_info(request, target_user):
    page = request.GET.get('page', 1)
    per_page = 2

    user_posts = Post.objects.filter(user_name=target_user).order_by('-created_at')
    pgt = Paginator(user_posts, per_page)
    try:
        contents = pgt.page(page)
    except PageNotAnInteger:
        contents = pgt.page(1)
    except EmptyPage:
        contents = []

    ctx = {
        'posts' : contents,
        'user' : target_user
    }
    return render(request, 'user_post_list.html', ctx)

    #return HttpResponse('{uname} 님'.format(uname=user_name))
