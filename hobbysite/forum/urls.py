from django.urls import path
from .views import list_view, detail_view

urlpatterns = [
    path('threads', list_view, name='post-category'),
    path('thread/<int:pk>', detail_view, name='post'),
]

app_name = 'forum'