from django.urls import path
from .views import list_view, detail_view, create_view, update_view

urlpatterns = [
    path('threads', list_view, name='post-category'),
    path('thread/<int:pk>', detail_view, name='post'),
    path('thread/add', create_view, name="thread-add"),
    path('thread/<int:pk>/edit', update_view, name="thread-edit")
]

app_name = 'forum'