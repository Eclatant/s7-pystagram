from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.conf.urls.static import static
from django.conf import settings

from photos import views


urlpatterns = [
    url(r'^photos/', include('photos.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login,
        {'template_name': 'login.html'}, name='login_url'),
    url(r'^logout/$', logout,
        {'next_page': '/login/'}),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

