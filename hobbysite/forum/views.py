from django.shortcuts import render, HttpResponse, redirect
from .models import Thread, ThreadCategory, Comment
from django.contrib.auth.decorators import login_required
from .forms import ThreadForm, CommentsForm

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
