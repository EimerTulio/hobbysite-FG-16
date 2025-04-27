from django.urls import path
from .views import article_list, article_detail

urlpatterns = [
path('articles', article_list, name="article/list"),
path('article/<int:pk>', article_detail, name="article/detail"),
]
# This might be needed, depending on your Django version
app_name = "wiki"
