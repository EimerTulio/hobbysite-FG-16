from django.urls import path

from .views import merch_list, merch_details, merch_create, merch_update, merch_cart, merch_transactions

urlpatterns = [
    path('items', merch_list, name='merch-list'),
    path('item/<int:pk>', merch_details, name='merch-detail'),
    path('item/add', merch_create, name='merch-create'),
    path('item/<int:pk>/edit', merch_update, name='merch-update'),
    path('cart', merch_cart, name='merch-cart'),
    path('transactions', merch_transactions, name='merch-transactions'),
]

app_name = "merchstore"
