from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm, RegisterForm

"""
Renders the unauthorized.html template when user attempts to perform action that requires login authentication
"""
def unauthorized_access(request):
    return render(request, 'user_management/unauthorized.html')

"""
Handles user registration. 
Checks for duplicate usernames or emails, creates a new user and associated profile, logs the user in, and redirects to the profile creation page upon success.
Displays error if validation fails.
"""
def profile_register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Extract username from the form data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'This username is already taken.')
                return render(request, 'user_management/profile_register.html', {'form': form})
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Email is already associated with another account.')
                return render(request, 'user_management/profile_register.html', {'form': form})

            # Save the user and create an associated profile
            user = form.save()
            Profile.objects.create(user=user, email=user.email)  # Create the profile with the user's email
            login(request, user)
            return redirect('user_management:profile-add')  # Redirect to the profile creation page
    else:
        form = RegisterForm()

    return render(request, 'user_management/profile_register.html', {'form': form})

"""
Allows authenticated users to create a profile.
Validates the profile form, associates the profile with the logged-in user, and redirects to the homepage upon success.
Displays an error if the user already has a profile.
"""
@login_required
def profile_create_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            if hasattr(request.user, 'profile'):
                form.add_error(None, "A profile with this user already exists.")
                return redirect('user_management:profile-update', username=request.user.username)
            profile = form.save(commit=False)
            profile.user = request.user  # Associate with logged in user
            profile.save()
            return redirect('homepage:index')
    else:
        form = ProfileForm()

    return render(request, 'user_management/profile_add.html', {'form': form})

"""
Enables authenticated users to update their profile.
Validates the form data, ensures only the profile owner can make changes, and redirects to the homepage upon success.
Renders the update form with existing profile data for editing.
"""
@login_required
def profile_update_view(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect('user_management:forbidden')  # or handle unauthorized access

    profile = user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('homepage:index')  # or any success page
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'user_management/profile_update.html', {'form': form})