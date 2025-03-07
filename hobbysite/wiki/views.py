from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import ArticleCategory, Article

class ArticleListView(ListView):
    model = ArticleCategory
    template_name = 'article_list.html'
    
class ArticleDetailView(DetailView):
    model = ArticleCategory
    template_name = 'article_detail.html'
    
def article_list(request):
    articles = ArticleCategory.objects.all()
    ctx = {
        "Articles" : articles
    }
    return render(request, 'article_list.html', ctx)

def article(request):
    article = Article.objects.all().order_by('-created_on')
    ctx = {
        "Article" : article
    }
    return render(request, 'article_detail.html', ctx)