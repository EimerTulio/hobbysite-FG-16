from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Product, Profile, Transaction
from .forms import TransactionForm, ProductForm

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
    user_id = request.user.id    
    form = TransactionForm()

    if (request.method == "POST"):
        form = TransactionForm(request.POST)

        if form.is_valid():
            t = Transaction()
            t.buyer = request.user.profile
            t.product = product
            t.amount = form.cleaned_data['amount']
            product.stock -= int(t.amount)
            if (product.stock <= 0):
                product.status = "O"
            t.save()
            product.save()
            if (request.user.is_authenticated):
                return HttpResponseRedirect(reverse('merchstore:merch-cart'))
            return HttpResponseRedirect(reverse('login'))

    ctx = {
        "product" : product,
        "user_id" : user_id,
        "form" : form,
    }

    return render(request, 'merchstore/merchstore_detail.html', ctx)

@login_required
def merch_create(request):
    """A view that allows the user to create a product."""

    form = ProductForm()

    if (request.method == "POST"):
        form = ProductForm(request.POST)

        if form.is_valid():
            p = ProductForm()
            p.owner = request.user.profile
            p.name = form.cleaned_data['name']
            p.description = form.cleaned_data['description']
            p.price = form.cleaned_data['price']
            p.product_type = form.cleaned_data['product_type']
            p.stock = form.cleaned_data['stock']
            p.status = form.cleaned_data['status']

    ctx = {
        "form" : form
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