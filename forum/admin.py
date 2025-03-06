from django.contrib import admin
from .models import PostCategory, Post


class PostCategoryAdmin(admin.ModelAdmin):
    model = PostCategory
    search_fields = ('name',)
    list_display = ('name',)
    fieldsets = [
        (
            'Post Category Information',
            {'fields': ['name', 'description']},
        ),
    ]


class PostAdmin(admin.ModelAdmin):
    model = Post
    search_fields = ('title',)
    list_display = ('title', 'time_created')
    fieldsets = [
        (
            'Posts Information',
            {'fields': ['title', 'entry', 'category']},
        ),
    ]


admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Post, PostAdmin)