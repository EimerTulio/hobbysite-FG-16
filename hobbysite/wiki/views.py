from django.shortcuts import render, get_object_or_404
from .models import ArticleCategory, Article

    
def article_list(request):
    '''Article list view for wiki articles'''
    articles = ArticleCategory.objects.all()
    ctx = {
        "articles" : articles
    }
    return render(request, 'wiki_list.html', ctx)

def article_detail(request, pk):
    '''Article detail view for wiki articles'''
    article = Article.objects.get(pk=pk)# .order_by('-created_on')
    ctx = {
        "article" : article
    }
    return render(request, 'wiki_detail.html', ctx)