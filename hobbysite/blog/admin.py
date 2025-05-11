from django.contrib import admin
from .models import Article, ArticleCategory

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_on', 'last_updated')


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory)

