from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView 

from .models import Product

# Create your views here.

class MerchListView(ListView):
    """A view that shows a list of merch."""
    model = Product
    template_name = 'merchstore/merchstore_list.html'

class MerchDetailView(DetailView):
    """A view that shows details about a product."""
    model = Product
    template_name = 'merchstore/merchstore_detail.html'
