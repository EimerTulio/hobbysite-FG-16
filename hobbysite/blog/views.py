from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from .models import Article, ArticleCategory
from .forms import CommentForm, ArticleForm
from django.utils.decorators import method_decorator
from user_management.models import Profile

# Create your views here.

"""
Displays a list of all articles, grouped by category and separating the current user's articles from others.
It returns the rendered blog_list.html template.
"""
def blog_list(request):
    all_articles = Article.objects.all().order_by('-created_on')
    user_articles = Article.objects.none() 
    
    if request.user.is_authenticated:
        user_articles = all_articles.filter(author__user=request.user)
        all_articles = all_articles.exclude(author__user=request.user)
    
    categories = ArticleCategory.objects.all().order_by('name')
    
    context = {
        'user_articles': user_articles,  
        'categories': categories,        
        'all_articles': all_articles,   
    }
    return render(request, 'blog/blog_list.html', context)

"""
Displays the details of a single article including comments and related articles.
Handles comment submission for authenticated users.
Along with the HttpRequest object (request), it takes in the ID of the specific article to be displayed (article_id)
It returns the rendered blog_detail.html template
"""
def blog_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = article.comment_set.all().order_by('created_on')
    related_articles = Article.objects.filter(author=article.author).exclude(id=article.id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user.profile
            comment.article = article
            comment.save()
    else:
        form = CommentForm()
    
    context = {
        'article': article,
        'related_articles': related_articles,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/blog_detail.html', context)

"""
Handles creation of new articles; only accessible to logged-in users.
Automatically sets the author to the current user's profile.
On GET: Empty article creation form
On POST: Redirect to article list if valid, or form with errors
"""
@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            profile = Profile.objects.get_or_create(user=request.user)
            article = form.save(commit=False)
            article.author = profile
            article.save()
            return redirect('blog:article_list')
    else:
        form = ArticleForm()
    
    return render(request, 'blog/article_form.html', {'form': form})

"""
Handles editing of existing articles; only accessible to the article's author.
Along with the HttpRequest object (request), it takes in the primary key of the specific article to edit (pk).
On GET: Pre-populated article edit form
On POST: Redirect to article list if valid, or form with errors
Redirects to article list if user is not the author
"""
@login_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if article.author.user != request.user:
        return redirect('blog:article_list')
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('blog:article_list')
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'blog/article_form.html', {'form': form})