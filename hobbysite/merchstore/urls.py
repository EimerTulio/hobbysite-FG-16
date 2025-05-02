from django.urls import path

from .views import merch_list, merch_details

urlpatterns = [
    path('items', merch_list, name='merch-list'),
    path('item/<int:pk>', merch_details, name='merch-detail'),
]

app_name = "merchstore"