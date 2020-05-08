from django.contrib import admin
from django.utils.html import format_html

from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'content', 'id',)
    list_filter = ('date_posted', 'title', 'author', 'id')
    ordering = ('-date_posted',)
    search_fields = ('author', 'title', 'content')
    date_hierarchy = "date_posted"
    actions_on_top = True
    actions_on_bottom = True


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'comment_text', 'date_posted')
    list_filter = ('date_posted', 'comment_text', 'author', 'id')
    ordering = ('date_posted',)
    search_fields = ('author', 'article')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
