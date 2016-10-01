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
from django.urls import reverse_lazy


from .models import Post
from .forms import PostSimpleForm
from .forms import PostForm
from pystagram.sample_exceptions import HelloWorldError

from raven.contrib.django.raven_compat.models import client

from raven import Client

client = Client('https://197093fb157044a1a1a9e0960d89bc03:af5d77eb13e84b3bbfecdea05e5d7ef4@sentry.io/102943')


logger = logging.getLogger(__name__)


def hello_world(request):
    return HttpResponse('hello world')


def list_posts(request):
    logger.debug('로그로그하군!')
    logger.info('로깅로깅하구나!')
    logger.warning('워닝워닝하네!')
    logger.error('하악 에러.!')

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
        'posts': contents,
    }
    return render(request, 'list.html', ctx)


def view_post(request, pk):
    #post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    ctx = {
        'post': post
    }
    return render(request, 'view.html', ctx)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # post = Post()
            # post.content = form.cleaned_data['content']
            # post.save()
            post = form.save(commit=False)  # 위 세 줄을 한 줄로 줄임.
            post.user = request.user
            post.save()
            # url = reverse('photos:view_post', kwargs={'pk': post.pk})
            # return redirect(url)

            return redirect('photos:view_post', pk=post.pk)
    elif request.method == 'GET':
        form = PostForm()

    ctx = {
        'form': form,
    }

    return render(request, 'edit.html', ctx)


class ListPost(ListView):
    model = Post
    template_name = 'list.html'
    context_object_name = 'posts'
    paginate_by = 2

#list_posts = ListPost.as_view()


class CreatePost(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'edit.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

#create_post = login_required(CreatePost.as_view())

