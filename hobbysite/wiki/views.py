from django.shortcuts import render, redirect
from .models import ArticleCategory, Article, Comment, ArticleImage
from .forms import ArticleForm, CommentForm, ArticleDetailForm, ArticleImageForm
from django.contrib.auth.decorators import login_required

"""
Displays a list of all articles, grouped by category.
It returns the rendered wiki_list.html template.
"""


def article_list(request):
    '''Article list view for wiki articles'''
    articles = ArticleCategory.objects.all()
    ctx = {
        "articles": articles
    }
    return render(request, 'wiki_list.html', ctx)


"""
Displays the details of a single article including comments and related articles.
Handles comment submission for authenticated users.
Along with the HttpRequest object (request), it takes in the primary key of the specific article to be displayed (pk)
It returns the rendered wiki_detail.html template
"""


def article_detail(request, pk):
    '''Article detail view for wiki articles'''
    article = Article.objects.get(pk=pk)
    category = article.category
    comments = article.comment_article.all()
    images = ArticleImage.objects.filter(article=article)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user.profile
            comment.save()
            return redirect('wiki:article-detail', pk=article.pk)
    else:
        form = CommentForm()

    if category:  # Check if the article has a category so it won't get null.
        if request.user.is_authenticated:
            related_articles = category.article_category.exclude(pk=article.pk)
        else:
            related_articles = category.article_category.exclude(
                pk=article.pk).filter(author__isnull=True)
    else:
        related_articles = []

    ctx = {
        "article": article,
        "related_articles": related_articles,
        "comments": comments,
        "form": form,
        "images": images,
    }
    return render(request, 'wiki_detail.html', ctx)


"""
Handles creation of new articles; only accessible to logged-in users.
Automatically sets the author to the current user's profile.
On GET: Empty article creation form
On POST: Redirect to article list if valid, or form with errors
"""


def article_add(request):
    '''Article create view for wiki articles'''
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            if request.user.is_authenticated:
                article.author = request.user.profile
            else:
                article.author = None
            article.save()
            return redirect('wiki:article-list')

    ctx = {'form': form}
    return render(request, 'wiki_add.html', ctx)


"""
Handles editing of existing articles; only accessible to the article's author.
Along with the HttpRequest object (request), it takes in the primary key of the specific article to edit (pk).
On GET: Pre-populated article edit form
On POST: Redirect to article list if valid, or form with errors
Redirects to article list if user is not the author
"""


@login_required
def article_update(request, pk):
    '''Article update view for wiki articles'''
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArticleDetailForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
        # Handle multiple image uploads
        if 'image' in request.FILES:
            for img in request.FILES.getlist('image'):
                description = request.POST.get('description', '')
                ArticleImage.objects.create(
                    article=article, image=img, description=description)

        return redirect('wiki:article-detail', pk=article.pk)

    else:
        form = ArticleDetailForm(instance=article)

    ctx = {
        'form': form,
        'article': article
    }
    return render(request, 'wiki_update.html', ctx)
