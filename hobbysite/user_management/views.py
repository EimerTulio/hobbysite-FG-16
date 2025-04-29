from django.shortcuts import render, HttpResponse, redirect
from .models import Profile
from .forms import ProfileForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

@login_required
def profile_create_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Associate with logged in user
            profile.save()
            return redirect('wiki:articles/list')
    else:
        form = ProfileForm()

    return render(request, 'user_management/profile_add.html', {'form': form})


def profile_update_view(request):
    profile = request.user.profile  # Get the current user's profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('wiki')  # or redirect to 'user_management:profile'
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        "form": form,
    }
    return render(request, 'user_management/profile_update.html', context)

def profile_login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Debugging: Check if authenticate is returning a user
            print(f"Authenticating user: {username}")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('wiki:articles/list')  # Redirect to home or any page you want
            else:
                form.add_error(None, "Invalid username or password")
                print("Authentication failed: Invalid credentials")
    return render(request, 'user_management/profile_login.html', {'form': form})

def profile_logout_view(request):
    logout(request)
    return redirect('user_management:login')