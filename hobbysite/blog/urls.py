from . import views 
from django.urls import path

urlpatterns = [
    path('articles/', views.blog_list, name='article_list'),
    path('article/<int:article_id>/', views.blog_detail, name='article_detail'),
]

app_name = 'blog'