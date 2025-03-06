from django.urls import path
from .views import index_view, list_view, detail_view

urlpatterns = [
    path('', index_view, name='index'),
    path('forum/threads', list_view, name='post-category'),
    path('forum/thread/<int:pk>/', detail_view, name='post'),
]