from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)
from django.views import View
from django.views.generic import TemplateView

from .forms import LoginForm
from user_management.models import Profile

# Custom authentication views


class CustomView(LoginRequiredMixin, TemplateView):
    """Base template for authenticated-only pages (requires user authentication)"""
    template_name = "registration/login.html"
    redirect_field_name = "login"


class CustomLogoutView(View):
    """
    Handles user logout via POST request.
    Redirects to login page.
    """

    def post(self, request):
        logout(request)
        return redirect('accounts:login')


def logout_view(request):
    """
    FBV version for user logout.
    Also redirects to login page.
    """
    logout(request)
    return redirect('accounts:login')


class CustomPasswordReset(PasswordResetView):
    """
    Handles password reset requests.
    Generates and sends password reset emails to users.
    Redirects to page for password reset success (success_url).
    """
    template_name = "registration/password_reset_form.html"
    email_template_name = "registration/password_reset_email.html"
    success_url = "password_reset/done"


class CustomPasswordResetDone(PasswordResetDoneView):
    """
    Displays confirmation that password reset email was sent.
    """
    template_name = "registration/password_reset_done.html"


class CustomPasswordResetConfirm(PasswordResetConfirmView):
    """
    Handles the actual password reset form where users enter new password.
    Validates the reset token and updates the password if valid.
    """
    template_name = "registration/password_reset_confirm.html"
    success_url = "password_reset/complete"
