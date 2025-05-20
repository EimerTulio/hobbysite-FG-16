from django.contrib import admin

from .models import ThreadCategory, Thread, Comment


class ThreadCategoryAdmin(admin.ModelAdmin):
    """Lists all thread categories and their details."""
    model = ThreadCategory
    search_fields = ('name',)
    list_display = ('name',)
    fieldsets = [
        (
            'Thread Category Information',
            {'fields': ['name', 'description']},
        ),
    ]


class ThreadAdmin(admin.ModelAdmin):
    """Lists all threads and their details."""
    model = Thread
    search_fields = ('title',)
    list_display = ('title', 'time_created')
    fieldsets = [
        (
            'Threads Information',
            {'fields': ['title', 'entry', 'category', 'author', 'image']},
        ),
    ]


class CommentAdmin(admin.ModelAdmin):
    """Lists every comment posted and their details."""
    model = Comment
    search_fields = ('author', 'thread')
    list_display = ('author', 'thread')
    fieldsets = [
        (
            'Comment Information',
            {'fields': ['author', 'thread', 'entry']},
        ),
    ]


admin.site.register(ThreadCategory, ThreadCategoryAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Comment, CommentAdmin)
