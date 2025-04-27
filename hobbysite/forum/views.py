from django.shortcuts import render, HttpResponse
from .models import Post, PostCategory


def list_view(request):
    categories = PostCategory.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, 'forum_list.html', context)


def detail_view(request, pk):
    category = PostCategory.objects.get(pk=pk)
    context = {
        "category": category,
    }
    return render(request, 'forum_detail.html', context)