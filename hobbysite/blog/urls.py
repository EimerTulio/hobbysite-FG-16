from . import views 
from django.urls import path

urlpatterns = [
    path('articles/', views.ArticleList, name='article_list'),
    path('article/<int:article_id>/', views.ArticleDetail, name='article_detail'),
]