from django.shortcuts import render
from photos.models import Tag
from photos.models import Post
from photos.models import Comment

# Create your views here.

def mainpage(req):
	arr_posts = []
	qus_posts = Post.objects.all()
	qus_first = qus_posts.first()

	if qus_first is not None:
		for post in qus_posts:
			arr_posts.append(post)

	ctx = {}
	ctx['arr_posts'] = arr_posts

	return render(req, 'mainpage.html', ctx)