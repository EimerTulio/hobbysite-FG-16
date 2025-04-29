from django import forms
from .models import Profile
from django.contrib.auth import authenticate
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
        
        return cleaned_data