from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse

# 페이징에 관련된 장고 메서드
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from .models import Post
from .models import Coment

# Create your views here.

# 장고의 View 함수는 첫 번째 인자로 HTTP Request 객체를 받는다.
def hello_world(req):
	return HttpResponse('hello world')

def list_posts(req):
	"""
	Pagination 이전 코드
	ctx = {}
	num_perpage = 2

	# GET 방식의 파라미터에 page가 있으면 값을 가져오고 없으면 1로 리턴
	# num_page = num_page if isinstance(num_page, int) else int(num_page)

	try:
		num_page = req.GET.get('page', 1)
		num_page = num_page if isinstance(num_page, int) else int(num_page)
	except (TypeError, ValueError):
		num_page = 1

	arr_posts = Post.objects.all().order_by('-created_at')
	ctx['arr_posts'] = arr_posts[(num_page - 1) * num_perpage: num_page * num_perpage]

	return render(req, 'list.html', ctx)
	"""
	ctx = {}
	page = req.GET.get('page', 1)
	per_page = 5
	arr_posts = Post.objects.all().order_by('-created_at')

	# 페이지네이터 객체의 인자 : 1번째 - 이터레이터 객체 / 2번째 - 페이징 기준
	pgt = Paginator(arr_posts, per_page)

	try:
		contents = pgt.page(page)
	except PageNotAnInteger:
		contents = pgt.page(1)
	except EmptyPage:
		contents = []

	ctx['arr_posts'] = contents

	return render(req, 'list.html', ctx)

def view_post(req, pk):
	ctx = {}
	md_post = get_object_or_404(Post, pk=pk)
	ctx['post'] = md_post
	return render(req, 'view.html', ctx)

def create_post(req):
	ctx = {}
	if req.method == 'POST':
		form = req.POST
		content = form['content']
		post = Post()
		post.content = content
		post.save()

		#url = reverse('photos:view_post', kwargs={'pk' : post.pk})
		#return redirect(url)

		return redirect('photos:view_post', pk=post.pk)
	return render(req, 'edit.html', ctx)

# 댓글 추가 함수
def add_comment(req, pk):
	ctx = {}
	if req.method == 'POST':
		# 전달된 댓글정보 수집
		form = req.POST
		content = form['content']

		# 추가할 글의 쿼리셋 정보 얻어오기
		target_post = Post.objects.get(pk=pk)

		# 댓글 모델 인스턴스 생성
		input_comment = Coment()
		input_comment.content = content

		# Post 모델에 연결된 외래키에 모델 인스턴스 추가
		input_comment.post = target_post

		# 댓글정보 저장
		input_comment.save()

		return redirect('photos:view_post', pk=pk)
	return render(req, 'view.html', ctx)

# 댓글 삭제 함수
def del_comment(req, pk):
	ctx = {}
	if req.method == 'POST':
		form = req.POST
		comment_id = form['comment_pk']

		# 대상 댓글 검색
		target_comment = Coment.objects.get(pk=comment_id)

		# 댓글 삭제
		target_comment.delete()

		return redirect('photos:view_post', pk=pk)
	return render(req, 'view.html', ctx)