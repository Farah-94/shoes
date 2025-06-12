from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ProfileUpdateForm


@login_required
def profile_detail(request):
    return render(request, "user/profile.html")

# walkease/user/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def profile_detail(request):
    # Render the profile page
    return render(request, "user/profile.html")

@login_required
def update_profile(request):
    profile = request.user.profile  # Get the current user's profile
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user:profile_detail')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, "user/update_profile.html", {"form": form})

