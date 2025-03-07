from django.urls import path
from .views import index_view, list_view, detail_view

urlpatterns = [
    path('', index_view, name='index'),
    path('threads', list_view, name='post-category'),
    path('thread/<int:pk>/', detail_view, name='post'),
]

app_name = 'forum'