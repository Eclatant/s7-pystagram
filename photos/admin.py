from django.contrib import admin

from .models import Post
from .models import Comment
from .models import Tag

class CommentInlineAdmin(admin.StackedInline):
    model = Comment
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', )
    list_display_links = ('id', 'created_at', )
    ordering = ('-id', '-created_at', )
    inlines = (CommentInlineAdmin, )
    list_filter = ('tags', )
    search_fields = ('content', )
    date_hierarchy = 'created_at'

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
