from django.shortcuts import render
from django.http import HttpResponse

from .models import Product

# Create your views here.

def merch_list(request):
    """A view that shows the list of all products."""
    merch = Product.objects.all()
    user_id = request.user.id
    ctx = {
        "merch" : merch,
        "user_id" : user_id
    }
    return render(request, 'merchstore/merchstore_list.html', ctx)

def merch_details(request, pk):
    """A view that shows details about a product."""
    product = Product.objects.get(pk=pk)
    ctx = {
        "product" : product
    }
    return render(request, 'merchstore/merchstore_detail.html', ctx)

def merch_create(request):
    """A view that allows the user to create a product."""
    ctx = {
    }
    return render(request, 'merchstore/merchstore_create.html', ctx)

def merch_update(request, pk):
    """A view that allows the user to update a product's details."""
    product = Product.objects.get(pk=pk)
    ctx = {
        "product" : product
    }
    return render(request, 'merchstore/merchstore_update.html', ctx)

def merch_cart(request):
    """A view that lists all products in the user's cart."""
    ctx = {
    }
    return render(request, 'merchstore/merchstore_cart.html', ctx)

def merch_transactions(request):
    """A view that lists all transactions made with the user's store."""
    ctx = {
    }
    return render(request, 'merchstore/merchstore_transactions.html', ctx)