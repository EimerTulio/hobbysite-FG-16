from django.shortcuts import render, HttpResponse
from .models import Post, PostCategory


def index_view(request):
    return render(request, 'base.html')


def list_view(request):
    categories = PostCategory.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, 'forum/threads.html', context)


def detail_view(request, pk):
    category = PostCategory.objects.get(pk=pk)
    context = {
        "category": category,
    }
    return render(request, 'forum/thread/1.html', context)