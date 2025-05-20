from django.shortcuts import render


def index_view(request):
    """A view that shows the main/home page."""
    return render(request, 'homepage/home.html')
