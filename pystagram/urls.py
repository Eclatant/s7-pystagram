from django.conf.urls import url
from django.contrib import admin

from photos import views


urlpatterns = [
    url(r'^$', views.list_posts),
    url(r'^hello/$', views.hello_world),
    url(r'^admin/', admin.site.urls),
]

