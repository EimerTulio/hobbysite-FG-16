from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Product, Transaction
from .forms import TransactionForm, ProductForm


def merch_list(request):
    """
    Displays a list of all available products. 
    Retrieves all products from the database 
    and passes them to the template along with the current user's ID.
    """
    merch = Product.objects.all()
    user_id = request.user.id
    ctx = {
        "merch": merch,
        "user_id": user_id
    }
    return render(request, 'merchstore/merchstore_list.html', ctx)


def merch_details(request, pk):
    """
    Shows detailed information about a specific product. 
    Handles the transaction form submission, updates the product stock, 
    and redirects to the cart page after a successful purchase. 
    If the user is not authenticated, redirects to the login page.
    """
    product = get_object_or_404(Product, pk=pk)
    user_id = request.user.id
    form = TransactionForm()

    if request.method == "POST":
        form = TransactionForm(request.POST)
        form.set_product(product)

        if form.is_valid():
            t = Transaction()
            t.product = product
            t.amount = form.cleaned_data['amount']
            product.stock -= int(t.amount)
            if product.stock <= 0:
                product.status = "O"
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('login') + "?next=" + request.path)
            t.buyer = request.user.profile
            t.save()
            product.save()
            return HttpResponseRedirect(reverse('merchstore:merch-cart'))

    ctx = {
        "product": product,
        "user_id": user_id,
        "form": form,
    }

    return render(request, 'merchstore/merchstore_detail.html', ctx)


@login_required
def merch_create(request):
    """
    Allows authenticated users to create a new product. 
    Saves the product with the current user as the owner, 
    and redirects to the product detail page upon success.
    """
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            p = Product()
            p.owner = request.user.profile
            p.name = form.cleaned_data['name']
            p.description = form.cleaned_data['description']
            p.price = form.cleaned_data['price']
            p.product_type = form.cleaned_data['product_type']
            p.stock = form.update_stock()
            p.status = form.update_status()
            p.save()
            return HttpResponseRedirect(reverse('merchstore:merch-detail', args=[p.pk]))

    ctx = {
        "form": form,
    }
    return render(request, 'merchstore/merchstore_create.html', ctx)


@login_required
def merch_update(request, pk):
    """
    Enables authenticated users to update an existing product's details. 
    Updates the product, and redirects to the product detail page upon success.
    """
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(instance=product)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.description = form.cleaned_data['description']
            product.price = form.cleaned_data['price']
            product.product_type = form.cleaned_data['product_type']
            product.stock = form.cleaned_data['stock']
            product.status = form.update_status()
            product.save()
            return HttpResponseRedirect(reverse('merchstore:merch-detail', args=[pk]))

    ctx = {
        "product": product,
        "form": form,
    }
    return render(request, 'merchstore/merchstore_update.html', ctx)


@login_required
def merch_cart(request):
    """
    Displays all transactions (cart items) for the authenticated user. 
    Lists all transactions and passes them to the template along with the current user's ID.
    """
    transactions = Transaction.objects.all()
    user_id = request.user.id
    ctx = {
        "transactions": transactions,
        "user_id": user_id,
    }
    return render(request, 'merchstore/merchstore_cart.html', ctx)


@login_required
def merch_transactions(request):
    """
    Lists all transactions involving the authenticated user's store. 
    Retrieves all transactions and passes them to the template along with the current user's ID.
    """
    transactions = Transaction.objects.all()
    user_id = request.user.id
    ctx = {
        "transactions": transactions,
        "user_id": user_id,
    }
    return render(request, 'merchstore/merchstore_transactions.html', ctx)
