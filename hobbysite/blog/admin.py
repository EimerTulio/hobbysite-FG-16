from django.contrib import admin
from .models import Article, ArticleCategory, Comment
from user_management.models import Profile


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'category',
                    'created_on', 'updated_on')

    def author_name(self, obj):
        return obj.author.name
    author_name.short_description = 'Author'


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory)
admin.site.register(Comment)
