from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.decorators import login_required

from .models import Photo
from .forms import PhotoSimpleForm
from .forms import PhotoForm


def hello_world(request):
    return HttpResponse('hello world')


def list_photos(request):
    page = request.GET.get('page', 1)
    per_page = 2

    photos = Photo.objects.all().order_by('-created_at')
    pgt = Paginator(photos, per_page)

    try:
        contents = pgt.page(page)
    except PageNotAnInteger:
        contents = pgt.page(1)
    except EmptyPage:
        contents = []

    ctx = {
        'photos': contents,
    }
    return render(request, 'list.html', ctx)


def view_photo(request, pk):
    #photo = Photo.objects.get(pk=pk)
    photo = get_object_or_404(Photo, pk=pk)
    ctx = {}
    return render(request, 'view.html', ctx)


@login_required
def create_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST)
        if form.is_valid():
            # post = Post()
            # post.content = form.cleaned_data['content']
            # post.save()

            photo = form.save(commit=True)  # 위 세 줄을 한 줄로 줄임.
            photo.user = request.user
            photo.save()
            #url = reverse('photos:view_photo', kwargs={'pk': photo.pk})
            #return redirect(url)
            return redirect('photos:view_photo', pk=photo.pk)
    elif request.method == 'GET':
        form = PhotoForm()

    ctx = {
        'form': form,
    }

    return render(request, 'edit.html', ctx)


@login_required
def delete_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST)
        if form.is_valid():
            # post = Post()
            # post.content = form.cleaned_data['content']
            # post.save()
            photo = form.save(commit=False)  # 위 세 줄을 한 줄로 줄임.
            photo.user = request.user
            photo.save()
            # url = reverse('photos:view_post', kwargs={'pk': post.pk})
            # return redirect(url)
            return redirect('photos:view_photo', pk=photo.pk)
    elif request.method == 'GET':
        form = PhotoForm()

    ctx = {
        'form': form,
    }

    return render(request, 'edit.html', ctx)
@login_required
def create_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # post = Post()
            # post.content = form.cleaned_data['content']
            # post.save()
            comment = form.save(commit=False)  # 위 세 줄을 한 줄로 줄임.
            comment.user = request.user
            photo.save()
            # url = reverse('photos:view_post', kwargs={'pk': post.pk})
            # return redirect(url)
            return redirect('photos:view_photo', pk=photo.pk)
    elif request.method == 'GET':
        form = PhotoForm()

    ctx = {
        'form': form,
    }

    return render(request, 'edit.html', ctx)




@login_required
def delete_comment(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST)
        if form.is_valid():
            # post = Post()
            # post.content = form.cleaned_data['content']
            # post.save()
            photo = form.save(commit=False)  # 위 세 줄을 한 줄로 줄임.
            photo.user = request.user
            photo.save()
            # url = reverse('photos:view_post', kwargs={'pk': post.pk})
            # return redirect(url)
            return redirect('photos:view_photo', pk=photo.pk)
    elif request.method == 'GET':
        form = PhotoForm()

    ctx = {
        'form': form,
    }

    return render(request, 'edit.html', ctx)
