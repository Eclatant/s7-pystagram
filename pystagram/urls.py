from django.conf.urls import url
from django.contrib import admin

from photos.views import hello_world


urlpatterns = [
    url(r'^hello/$', hello_world),
    url(r'^admin/', admin.site.urls),
]

