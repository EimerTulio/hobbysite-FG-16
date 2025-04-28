from django.shortcuts import render, HttpResponse, redirect
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm

@login_required
def profile_create_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Associate with logged in user
            profile.save()
            return redirect('user_management:profile')
    else:
        form = ProfileForm()

    return render(request, 'user_management/profile_form.html', {'form': form})


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
    return render(request, 'user_management/profile.html', context)
def profile_login_view(request):
    
    return render(request, 'user_management/profile.html', context)
