from . import views 
from django.urls import path
from .views import (blog_list, blog_detail, ArticleCreateView, ArticleUpdateView)

urlpatterns = [
    path('articles/', blog_list, name='article_list'),
    path('article/<int:article_id>/', blog_detail, name='article_detail'), 
    path('article/add/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
]