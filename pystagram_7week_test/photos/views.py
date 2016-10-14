import logging
# 표준라이브러리 import

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView
from django.views.generic import View
from django.views.generic import CreateView
from django.contrib.auth import get_user_model

# 설치한 라이브러리 import

from .models import Photo, Comment, Like
from profiles.models import Profile, Follow
from .forms import PostSimpleForm
from .forms import PhotoForm, CommentForm, PhotoDeleteForm, CommentDeleteForm
from pystagram.sample_exceptions import HelloWorldError
# 프로젝트에서 생성한 요소들 import

# from raven.contrib.django.raven_compat import client
from raven import Client

client = Client('https://c41324a4173643f3b6fe4142d1dfefe6:5251348a010b46319ea67273b8d8f31b@sentry.io/102944')
logger = logging.getLogger(__name__)

user_model_class = get_user_model()

def hello_world(request):
    return HttpResponse('hello_world')

# def list_photos(request):
#     #try:
#     #    raise HelloWorldError('error error')
#     #except Exception:
#     #    client.captureException()
#
#     # logger.debug('debug logging')
#     # logger.info('info logging')
#     # logger.warning('warning logging')
#     # logger.error('error logging')
# #    raise HelloWorldError('오류다~')
#
#     # print('-'*40)
#     # print(request.just_say)
#     # print('-'*40)
#
#     page = request.GET.get('page',1)
#     per_page = 2
#
# #    try:
# #        page = request.GET.get('page', '')
# #        if page.isdigit():
# #            page = int(page)
# #        if page < 1:
# #            page = 1
# #    # page = request.GET['page'] 는 page가 입력되지 않을 때 오류가 남
# #    except (TypeError, ValueError):
# #        page = 1
#
#     photos = Photo.objects.all().order_by('-created_at')
#     pgt = Paginator(photos, per_page)
#
#     try :
#         contents = pgt.page(page)
#     except PageNotAnInteger:
#         contents = pgt.page(1)
#     except EmptyPage:
#         contents = []
#
#     ctx = {
#         'photos' : contents,
# #        'photos': photos[(page-1)*per_page:page*per_page]
#     }
#     return render(request, 'list.html', ctx)


def view_photo(request, pk):
    # post = Post.objects.get(pk=pk)
    # django가 이 경우에 대해서는 pk를 string -> int로 전환해줌
    photo = get_object_or_404(Photo, pk=pk)
    
    """
    model에 selection field가 있는 경우

        like = 0
        try :
            if photo.like_set.get(user = request.user).selection:
                like = 1
        except TypeError:
            return redirect('login_url')
        except Like.DoesNotExist:
            pass
    """

    ctx = {
        'photo': photo,
    }

    return render(request, 'view.html', ctx)

@login_required
def create_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        # request.FILES 로 해야 업로드 파일이 전달됨
        if form.is_valid():
            # post = Post()
            # post.content = form.cleaned_data['content']
            # post.save()
            photo = form.save(commit=False) #commit=False를 지울경우, 위 세줄을 한 줄로 줄임
            photo.user = request.user
            photo.save()
            return redirect('photos:view_photo', pk=photo.pk)
        # form = request.POST
        # content = form['content']
        # url = reverse('photos:view_photo',kwargs={'pk':post.pk})
        # return redirect(url)
    elif request.method == 'GET':
        form = PhotoForm()

    ctx = {
       'form' : form,
    }
    return render(request, 'edit.html', ctx)

@login_required
def create_comment(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
#        comment.post = Post.objects.filter(pk=pk)[0] 
            comment.photo = get_object_or_404(Photo, pk=pk)
            comment.photo.user = request.user
            comment.save()

# ajax 처리시
#            if request.is_ajax():
#                return JsonResponse({'result':True})
#            else :
#                return redirect('photos:view_photo', pk=pk)

            return redirect('photos:view_photo', pk=pk)
    elif request.method == 'GET':
        form = CommentForm()

    ctx = {
            'form' : form,    
    }
    return render(request, 'edit.html', ctx)

@login_required
def delete_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)

    if request.user != photo.user:
    #if request.user.username == 'test2':
        raise PermissionDenied

    if request.method == 'POST':

        form = PhotoDeleteForm(request.POST)
        if form.is_valid():
            photo.delete()
            return redirect('photos:list_photos')
    ctx = {
        'item':photo
    }
    return render(request, 'comment_delete.html', ctx)

@login_required
@permission_required('photos.delete_Comment', raise_exception=True)
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if request.method == 'POST':
        form = CommentDeleteForm(request.POST)
        if form.is_valid():
            comment.delete()
            return redirect('photos:view_photo', pk=comment.photo_id)
    ctx = {
        'item':comment
    }
    return render(request, 'comment_delete.html', ctx)

class ListPost(ListView):
    model = Photo
    template_name = 'list.html'
    paginate_by = 4


    def get_context_data(self, **kwargs):
        context = super(ListPost, self).get_context_data(**kwargs)
        queryset = Photo.objects.order_by('-created_at')
        pgt = Paginator(queryset, self.paginate_by)

        page = self.request.GET.get('page', 1)

        try :
            contents = pgt.page(page)
        except PageNotAnInteger:
            contents = pgt.page(1)
        except EmptyPage:
            contents = []

        context['photos'] = contents
        return context


# class CreatePost(createView, JsonResponseMixin):
# class로 ajax 처리를 따로 class를 만들어서 처리하기도 함

# class CreatePost(CreateView):
#     model = Photo
#     form = PhotoForm
#     template_name = 'edit.html'
#
#
#     # 이전 django 버전에서는 에러가 발생하기 때문에 아래를 포함해야했음
#     def form_valid(self, form_class):
#         form_class.instance.user = self.request.user
#         return super().form_valid(form_class)
#
#     # get_absolute_url이 models.py에 있을 경우에 자동으로 해당 url로 redirect됨
#     # success_url = reverse_lazy('photos:view_photo') 할당
#     # def get_success_url : return reverse('photos:view_photo')함수 정의
#
# create_photo = login_required(CreatePost.as_view())


@login_required
def like(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    qs = photo.like_set.filter(user=request.user)
    did_like = qs.exists()

    if did_like :
        qs.delete()
        res_text = '좋아요 취소'
    else :
        qs.create(photo = photo, user=request.user)
        res_text = '좋아요'

#    return HttpResponse(res_text)
    return redirect('photos:view_photo', pk=pk)

"""
model에 좋아요 여부인 selection field가 있는 경우

try :
   like = photo.like_set.get(user=request.user)
   if like.selection :
       like.selection = 0
   else :
       like.selection = 1
   like.save()
except Like.DoesNotExist :
   like = Like()
   like.user = request.user
   like.photo = photo
   like.selection = 1
   like.save()
return redirect('photos:view_photo', pk=pk)

"""


class UserProfile(ListView):
    model = Profile
    template_name = 'user_profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        user = self.kwargs['pk']

        user_profile = get_object_or_404(Profile, user=user)
        following_num = user_profile.follow_set.count()
        follower_num = Follow.objects.filter(user=user).count()

        context = {
            'user_profile':user_profile,
            'login_user':self.request.user,
            'following_num':following_num,
            'follower_num':follower_num,
        }
        return context

class Follows(View):

    def get(self, request, *args, **kwargs):
        return redirect('photos:list_photos')


    def post(self, request, *args, **kwargs):

        follower = self.request.user.profile.pk
        following = self.request._post['user']

        if request.user.pk != following:
            profile = get_object_or_404(Profile, pk=follower)
            qs = profile.follow_set.filter(user=following)
            did_follow = qs.exists()

            if did_follow :
                qs.delete()
                res_text = '팔로우'
            else :
                following_user = get_object_or_404(user_model_class, pk=following)
                qs.create(follower=profile, user=following_user)
                res_text = '팔로우 취소'

            return HttpResponse(res_text)

        else:
            return HttpResponse('error')
