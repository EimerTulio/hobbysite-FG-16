from django.urls import path
from .views import article_list, article_detail, article_add, article_update

urlpatterns = [
path('articles', article_list, name="article-list"),
path('article/<int:pk>', article_detail, name="article-detail"),
path('article/add', article_add, name="article-add"),
path('article/<int:pk>/edit', article_update, name="article-update"),
]
# This might be needed, depending on your Django version
app_name = "wiki"
