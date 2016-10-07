from django.conf.urls import url
from . import views

app_name = 'photos'

urlpatterns = [
    url(r'^$', views.list_photos, name = 'list_photos'),
    url(r'^(?P<pk>[0-9]+)/$', views.view_photo, name = 'view_photo'),
    url(r'^hello/$', views.hello_world),
    url(r'^create/$', views.create_photo, name='create_photo'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.delete_photo, name='delete_photo'),
    url(r'^(?P<pk>[0-9]+)/comment/create/$', views.create_comment, name='create_comment'),
    url(r'^comment/(?P<comment_id>[0-9]+)/delete/$', views.delete_comment, name='delete_comment'),
    url(r'^(?P<pk>[0-9]+)/like/create/$', views.create_like, name='create_like'),
]
