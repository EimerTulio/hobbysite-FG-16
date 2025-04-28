from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Article, ArticleCategory

# Create your views here.

def ArticleList(request):
    articles = Article.objects.all()  
    return render(request, 'blog/index.html', {'articles': articles})

def ArticleDetail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'blog/blog_detail.html', {'article': article})