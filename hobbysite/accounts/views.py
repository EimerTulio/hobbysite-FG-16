from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm
from user_management.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)
from django.views import View
from django.views.generic import TemplateView

# Custom authentication views
"""
Base template for authenticated-only pages (requires user authentication)
"""
class CustomView(LoginRequiredMixin, TemplateView):
    template_name = "registration/login.html"
    redirect_field_name = "login"

"""
Handles user logout via POST request.
Redirects to login page
"""
class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('accounts:login')

"""
FBV version for user logout
Also redirects to login page
"""
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

"""
Handles password reset requests.
Generates and sends password reset emails to users.
Redirects to page for password reset success (success_url)
"""
class CustomPasswordReset(PasswordResetView):
    template_name = "registration/password_reset_form.html"
    email_template_name = "registration/password_reset_email.html"
    success_url = "password_reset/done"

"""
Displays confirmation that password reset email was sent.
"""
class CustomPasswordResetDone(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"

"""
Handles the actual password reset form where users enter new password.
Validates the reset token and updates the password if valid.
"""
class CustomPasswordResetConfirm(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    success_url = "password_reset/complete"