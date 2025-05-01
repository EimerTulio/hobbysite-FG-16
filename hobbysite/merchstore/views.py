from django.shortcuts import render
from django.http import HttpResponse

from .models import Product

# Create your views here.

def merch_list(request):
    """A view that shows the list of all products."""
    merch = Product.objects.all()
    ctx = {
        "merch" : merch
    }
    return render(request, 'merchstore/merchstore_list.html', ctx)

def merch_details(request, pk):
    """A view that shows details about a product."""
    product = Product.objects.get(pk=pk)
    ctx = {
        "product" : product
    }
    return render(request, 'merchstore/merchstore_detail.html', ctx)
