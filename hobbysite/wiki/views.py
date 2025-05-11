from django.shortcuts import render, redirect
from .models import ArticleCategory, Article
from .forms import ArticleForm, CommentForm

    
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

def article_add(request):
    '''Article create view for wiki articles'''
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():# https://stackoverflow.com/questions/68389156/django-how-to-set-user-create-article-is-by-user-is-logon
            article = form.save(commit=False)
            article.author = request.user.profile
            article.save()
            return redirect('wiki:article-list')
    
    ctx = {'form' : form}
    return render(request, 'wiki_add.html', ctx)

def article_update(request, pk):
    '''Article update view for wiki articles'''
    article = Article.objects.get(pk=pk)
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            return redirect('wiki:article-detail', article.pk)
    
    ctx = {
        'form' : form,
        'article' : article
    }
    return render(request, 'wiki_update.html', ctx)
