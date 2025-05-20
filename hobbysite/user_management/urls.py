from django.urls import path
from .views import profile_update_view, profile_create_view, profile_register_view, profile_detail_view, unauthorized_access

urlpatterns = [
    path('update/<str:username>', profile_update_view, name='profile-update'),
    path('create', profile_create_view, name='profile-add'),
    path('register', profile_register_view, name='profile-register'),
    path('forbidden', unauthorized_access, name="forbidden"),
    path('<str:username>', profile_detail_view, name="profile-detail"),
]

app_name = 'user_management'