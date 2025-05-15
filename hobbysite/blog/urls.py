from . import views
from django.urls import path
from .views import (blog_list, blog_detail, article_create, article_update)

urlpatterns = [
    path('articles/', views.blog_list, name='article_list'),
    path('article/<int:article_id>/', views.blog_detail, name='article_detail'),
    path('article/add/', article_create, name='article_create'),
    path('article/<int:pk>/edit/', article_update, name='article_update'),
]

app_name = 'blog'
