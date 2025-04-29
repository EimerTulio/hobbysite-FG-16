from django.urls import path
from .views import profile_update_view, profile_login_view, profile_create_view, profile_logout_view

urlpatterns = [
    path('profile', profile_update_view, name='profile-update'),
    path('login', profile_login_view, name='login'),
    path('add', profile_create_view, name='profile-add'),
    path('logout', profile_logout_view, name='logout'),
]

app_name = 'user_management'