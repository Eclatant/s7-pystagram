from django.contrib import admin

from .models import Post
from .models import Comment
from .models import Tag


class PostAdmin(admin.ModelAdmin):
    list_filter = ('tags', )


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Tag)

