from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'photos'

urlpatterns = [
    url(r'^$', login_required(views.ListPost.as_view()), name = 'list_photos'),
    url(r'^(?P<pk>[0-9]+)/$', views.view_photo, name = 'view_photo'),
    url(r'^hello/$', views.hello_world),
    url(r'^create/$', views.create_photo, name='create_photo'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.delete_photo, name='delete_photo'),
    url(r'^(?P<pk>[0-9]+)/comment/create/$', views.create_comment, name='create_comment'),
    url(r'^comment/(?P<comment_id>[0-9]+)/delete/$', views.delete_comment, name='delete_comment'),
    url(r'^(?P<pk>[0-9]+)/like/$', views.like, name='like'),
    url(r'^user/(?P<pk>[0-9]+)/$', login_required(views.UserProfile.as_view()), name = 'user_profile'),
    url(r'^user/follow', login_required(views.Follows.as_view()), name = 'follow'),
]
