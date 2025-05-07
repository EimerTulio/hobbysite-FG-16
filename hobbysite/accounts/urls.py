from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetCompleteView
from .views import logout_view
from accounts.views import (
    CustomView,
    CustomPasswordReset,
    CustomPasswordResetDone,
    CustomPasswordResetConfirm,
    CustomLogoutView
)


urlpatterns = [
    path("login/", CustomView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("password_reset", CustomPasswordReset.as_view(), name="password_reset"),
    path(
        "password_reset/<uidb64>/<token>/",
        CustomPasswordResetConfirm.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/done",
        CustomPasswordResetDone.as_view(),
        name="password_reset_done",
    ),
    path(
        "password_reset/complete",
        PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]


app_name = "accounts"