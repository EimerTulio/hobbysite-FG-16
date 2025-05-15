from django.shortcuts import render, HttpResponse, redirect
from .models import Thread, ThreadCategory, Comment
from django.contrib.auth.decorators import login_required
from .forms import ThreadForm, CommentsForm

"""
Displays a list of all threads, grouped by category and separating the current user's articles from others.
It returns the rendered forum_list.html template.
"""
def list_view(request):
    if request.user.is_authenticated == True:
        current_user = request.user.profile
        user_threads = Thread.objects.filter(author=current_user)
        other_threads= Thread.objects.exclude(author=current_user)
        other_categories = ThreadCategory.objects.filter(post_category__in=other_threads).distinct()
    else:
        user_threads = Thread.objects.none()
        other_threads = Thread.objects.none()
        other_categories = ThreadCategory.objects.none()
    categories = ThreadCategory.objects.all()
    context = {
        "user_threads": user_threads,
        "other_categories": other_categories,
        "other_threads": other_threads,
        "categories": categories,
    }
    return render(request, 'forum/forum_list.html', context)


from django.shortcuts import render, get_object_or_404

"""
Displays the details of a single thread including comments and related threads of the same category.
Handles comment submission for authenticated users
Along with the HttpRequest object (request), it takes in the primary key of the specific article to be displayed (pk)
It returns the rendered forum_detail.html template
"""
def detail_view(request, pk):
    threads = get_object_or_404(Thread, pk=pk)
    related_threads = Thread.objects.filter(category=threads.category).exclude(pk=threads.pk)
    profile= None
    comments = Comment.objects.filter(thread = threads)
    if request.user.is_authenticated:
        profile = request.user.profile
    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = threads
            comment.author = request.user.profile
            comment.save()
    else:
        form = CommentsForm()
    context = {
        "thread": threads, 
        "form": form,
        "profile": profile,
        "related_threads": related_threads, 
        "comments": comments
    }
    return render(request, 'forum/forum_detail.html', context)

"""
Handles creation of new threads; only accessible to logged-in users.
Automatically sets the author to the current user's profile.
On GET: Empty thread creation form
On POST: Redirect to thread list if valid, or form with errors
"""
@login_required
def create_view(request):
    form = ThreadForm()

    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            if request.user.is_authenticated:
                thread.author = request.user.profile
            thread.save()
            return redirect("forum:post", pk=thread.pk)

    context = {"form": form}
    return render(request, "forum/forum_add.html", context)

"""
Handles editing of existing threads; only accessible to the thread's author.
Along with the HttpRequest object (request), it takes in the primary key of the specific thread to edit (pk).
On GET: Pre-populated thread edit form
On POST: Redirect to thread list if valid, or form with errors
Redirects to thread list if user is not the author
"""
def update_view(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    form = ThreadForm()
    if request.method == "POST":
        form = ThreadForm(request.POST, request.FILES, instance=thread)
        if form.is_valid():
            form.save()
            return redirect("forum:post", pk=thread.pk)
        
    else:
        form = ThreadForm(instance=thread)
    context = {"form": form, 
               "thread": thread,
               }
    return render(request, "forum/forum_edit.html", context)
