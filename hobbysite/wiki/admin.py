from django.contrib import admin
from .models import ArticleCategory, Article, Comment
# Register your models here.

class ArticleInline(admin.TabularInline):
    '''Inline for ArticleCategory'''
    model = Article
    extra = 1
    
class ArticleCategoryAdmin(admin.ModelAdmin):
    '''Admin for ArticleCategory'''
    ordering = ['name']
    inlines = [
        ArticleInline,
    ]
    
class CommentAdmin(admin.ModelAdmin):
    model = Comment

admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Comment)
