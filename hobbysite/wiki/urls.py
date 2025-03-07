from django.urls import path
from .views import ArticleListView, ArticleDetailView

urlpatterns = [
path('wiki/articles', ArticleListView.as_view(), name="article/list"),
path('wiki/article/<int:pk>', ArticleDetailView.as_view(), name="article/detail"),
]
# This might be needed, depending on your Django version
app_name = "wiki"
