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
    return HttpResponse('hello_world')

def list_posts(request):
    page = request.GET.get('page',1)
    per_page = 2

#    try:
#        page = request.GET.get('page', '')
#        if page.isdigit():
#            page = int(page)
#        if page < 1:
#            page = 1
#    # page = request.GET['page'] 는 page가 입력되지 않을 때 오류가 남
#    except (TypeError, ValueError):
#        page = 1

    posts = Post.objects.all().order_by('-created_at')
    pgt = Paginator(posts, per_page)

    try :
        contents = pgt.page(page)
    except PageNotAnInteger:
        contents = pgt.page(1)
    except EmptyPage:
        contents = []

    ctx = {
        'posts' : contents,
#        'posts': posts[(page-1)*per_page:page*per_page] 
    }
    return render(request, 'list.html', ctx)

def view_post(request, post_id):
    # post = Post.objects.get(pk=pk)
    # django가 이 경우에 대해서는 pk를 string -> int로 전환해줌
    post = get_object_or_404(Post, pk=post_id)
    ctx = {
        'post': post
    }
    return render(request, 'view.html', ctx)

def create_post(request):
    if request.method == 'POST':
        form = request.POST
        content = form['content']
        post = Post()
        post.content = content
        post.save()
        # url = reverse('photos:view_post',kwargs={'pk':post.pk})
        # return redirect(url)
        return redirect('photos:view_post', post_id=post.pk)
    ctx = {}
    return render(request, 'edit.html', ctx)

def create_comment(request, post_id):
    if request.method == 'POST':
        form = request.POST
        content = form['content']
        comment = Comment()
        comment.content = content
        comment.post = Post.objects.filter(pk=post_id)[0] 
        comment.save()
        return redirect('photos:view_post', post_id=post_id)
    ctx = {}
    return render(request, 'edit.html', ctx)

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('photos:view_post', post_id=comment.post_id)
    ctx = {
        'comment':comment
    }
    return render(request, 'comment_delete.html', ctx)
