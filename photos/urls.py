from django.conf.urls import url
from . import views as m_photo

app_name = 'photos'

urlpatterns = [
    url(r'^$', m_photo.list_posts),
    url(r'^create/$', m_photo.create_post, name='create'),
	url(r'^posts/(?P<pk>[0-9]+)/$', m_photo.view_post, name='view_post'),
    url(r'^posts/(?P<pk>[0-9]+)/addcomment$', m_photo.add_comment, name='addcomment'),
	url(r'^posts/(?P<pk>[0-9]+)/delcomment$', m_photo.del_comment, name='delcomment'),
]
