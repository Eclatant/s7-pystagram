from django.contrib import admin
from photos.models import *

# Register your models here.

admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)