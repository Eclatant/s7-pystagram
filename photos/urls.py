from django.conf.urls import url
from . import views

app_name = 'photos'

urlpatterns = [
    url(r'^$', views.list_posts),
    url(r'^posts/(?P<post_id>[0-9]+)/$', views.view_post, name = 'view_post'),
    url(r'^hello/$', views.hello_world),
    url(r'^posts/create/$', views.create_post, name='create'),
    url(r'^posts/(?P<post_id>[0-9]+)/comment/create/$', views.create_comment, name='create_comment'),
    url(r'^posts/comment/(?P<comment_id>[0-9]+)/delete/$', views.delete_comment, name='delete_comment')
]
