from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied

from .models import Photo, Comment
from .forms import PostSimpleForm
from .forms import PhotoForm, CommentForm, PhotoDeleteForm, CommentDeleteForm

def hello_world(request):
    return HttpResponse('hello_world')

def list_photos(request):
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

    photos = Photo.objects.all().order_by('-created_at')
    pgt = Paginator(photos, per_page)

    try :
        contents = pgt.page(page)
    except PageNotAnInteger:
        contents = pgt.page(1)
    except EmptyPage:
        contents = []

    ctx = {
        'photos' : contents,
#        'photos': photos[(page-1)*per_page:page*per_page] 
    }
    return render(request, 'list.html', ctx)

def view_photo(request, pk):
    # post = Post.objects.get(pk=pk)
    # django가 이 경우에 대해서는 pk를 string -> int로 전환해줌
    photo = get_object_or_404(Photo, pk=pk)
    ctx = {
        'photo': photo
    }
    return render(request, 'view.html', ctx)

@login_required
def create_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST)
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
            return redirect('photos:view_photo', pk=pk)
    elif request.method == 'GET':
        form = CommentForm()

    ctx = {
            'form' : form,    
    }
    return render(request, 'edit.html', ctx)

@login_required
def delete_photo(request, pk):
    if request.user.username == 'test2':
        raise PermissionDenied

    photo = get_object_or_404(Photo, pk=pk)

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
