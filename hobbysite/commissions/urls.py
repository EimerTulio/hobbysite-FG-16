from django.urls import path
from .views import commission_list, commission_detail

urlpatterns = [
    path('list/', commission_list, name = 'commission_list'),
    path('detail/<int:commission_id>/', commission_detail, name = 'commission_detail'),
]

app_name = "commissions"