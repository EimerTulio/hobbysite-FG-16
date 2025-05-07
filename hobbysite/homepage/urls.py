from django.urls import path
from .views import index_view

urlpatterns = [
    path('home/', index_view, name='index'),
]

app_name = 'homepage'