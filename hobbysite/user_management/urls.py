from django.urls import path
from .views import profile_update_view, profile_login_view, profile

urlpatterns = [
    path('', profile_update_view, name='profile'),
    path('/login', profile_login_view, name='profile'),
    path('/register', profile_register_view, name='profile'),
    path('/logout', profile_logout_view, name='profile'),
]

app_name = 'user_management'