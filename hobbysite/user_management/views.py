from .models import Profile
from .forms import ProfileForm, LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def profile_register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('homepage:index')
    else:
        form = RegisterForm()

    return render(request, 'user_management/profile_register.html', {'form': form})

@login_required
def profile_create_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Associate with logged in user
            profile.save()
            return redirect('homepage:index')
    else:
        form = ProfileForm()

    return render(request, 'user_management/profile_add.html', {'form': form})

@login_required
def profile_update_view(request):
    profile = request.user.profile 
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('homepage:index') 
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

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('homepage:index') 
            else:
                form.add_error(None, "Invalid username or password")
                print("Authentication failed: Invalid credentials")
    return render(request, 'user_management/profile_login.html', {'form': form})

def profile_logout_view(request):
    logout(request)
    return redirect('user_management:login')