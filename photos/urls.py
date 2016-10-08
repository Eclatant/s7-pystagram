from django.conf.urls import url

from . import views


app_name = 'photos'

urlpatterns = [
    url(r'^$', views.list_posts),
    url(r'^create/$', views.create_post, name='create'),
    url(r'^posts/(?P<pk>[0-9]+)/$', views.view_post, name='view_post'),
    url(r'^posts/(?P<pk>[0-9]+)/like/$', views.like, name='like'),
]

