from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Article, ArticleCategory

# Create your views here.

def blog_list(request):
    articles = Article.objects.all()  
    return render(request, 'blog/blog_list.html', {'articles': articles})

def blog_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'blog/blog_detail.html', {'article': article})