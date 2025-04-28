from django.shortcuts import render, HttpResponse, redirect
from .models import Thread, ThreadCategory
from django.contrib.auth.decorators import login_required
from .forms import ThreadForm

def list_view(request):
    categories = ThreadCategory.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, 'forum/forum_list.html', context)


from django.shortcuts import render, get_object_or_404

def detail_view(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    context = {
        "thread": thread,
    }
    return render(request, 'forum/forum_detail.html', context)

def create_view(request):
    form = ThreadForm()

    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save()
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
