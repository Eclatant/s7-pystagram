from django.conf.urls import url

from . import views


app_name = 'photos'

urlpatterns = [
    url(r'^create_photo/$', views.create_photo, name='create_photo'),
    url(r'^delete_photo/$', views.delete_photo, name='delete_photo'),
    url(r'^view_photo/(?P<pk>[0-9]+)/$', views.view_photo, name='view_photo'),
    url(r'^list_photos/$', views.list_photos, name='list_photos'),
    url(r'^create_comment/$', views.create_comment, name='create_comment'),
    url(r'^delete_comment/$', views.delete_comment, name='delete_comment'),
]

