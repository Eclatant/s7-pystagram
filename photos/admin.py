from django.contrib import admin
from photos.models import Post
from photos.models import Comment
from photos.models import Tag

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)

