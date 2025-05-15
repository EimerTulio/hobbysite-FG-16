from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    """A form that allows a user to log in."""
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        """Authenticates a user and returns the entered details."""
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")

        return cleaned_data
