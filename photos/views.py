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
def add_like(request, pk): # 추가 업데이트해야될내용: 글쓴이는 좋아요를 할 수없어야한다
    post = get_object_or_404(Post, pk=pk)
    like_user = post.like_set.filter(user=request.user)
    ctx = { 'post': post }
    #if request.method == 'POST':
    #    like = Like()
    #    like.post = post
    #    like.save()
    if like_user.exists():
        print('이미 좋아요를 누르셨습니다!')
        return render(request, 'like_impossible.html', ctx)
    else:
        like = Like()
        like.user = request.user
        like.post = post
        like.save()
        return redirect('photos:view_post', pk=post.pk)

"""
class ListPost(ListView):
    model = Post
    template_name = 'list.html'
    context_object_name = 'posts'
    paginate_by = 2

list_posts = ListPost.as_view()

class CreatePost(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'edit.html'

    def form_valid(self, form):
        form.instance = self.request.user
        return super()
    #success_url = reverse_lazy('photos:view_post')

create_post = login_required(CreatePost.as_view())
"""
