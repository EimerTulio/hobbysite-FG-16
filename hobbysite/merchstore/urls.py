from django.urls import path

from .views import MerchListView, MerchDetailView

urlpatterns = [
    path('/items', MerchListView.as_view(), name='merch-list'),
    path('/item/<int:id>', MerchDetailView.as_view(), name='merch-detail'),
]

app_name = "merchstore"