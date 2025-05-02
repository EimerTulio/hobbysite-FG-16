from django.contrib import admin
from .models import ArticleCategory, Article
# Register your models here.

class ArticleInline(admin.TabularInline):
    model = Article
    extra = 1
    
class ArticleCategoryAdmin(admin.ModelAdmin):
    inlines = [
        ArticleInline,
    ]    
admin.site.register(ArticleCategory, ArticleCategoryAdmin)

