from django.conf.urls import url

from . import views

app_name = 'photos'

urlpatterns = [
    url(r'^$', views.list_posts, name='list_post'),
    url(r'^create/$', views.create_post, name='create'),
    url(r'^posts/(?P<pk>[0-9]+)/$', views.view_post, name='view_post'),
    url(r'^posts/(?P<pk>[0-9]+)/(?P<post_pk>[0-9]+)/delete_comment/$', views.delete_comment, name='delete_comment'),
    url(r'^posts/(?P<pk>[0-9]+)/create_comment/$', views.create_comment, name='create_comment'),
    url(r'^posts/(?P<pk>[0-9]+)/add_like/$', views.add_like, name='add_like'),
    url(r'^user_info/(?P<target_user>\w+)/$', views.user_info, name='user_info'),
]
