from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
    # For now, just a placeholder that renders an update template.
    # Later, you might integrate a ModelForm to handle the update logic.
    if request.method == "POST":
        # Process form data here...
        # form = UserProfileForm(request.POST, instance=request.user.profile)
        # if form.is_valid():
        #     form.save()
        #     return redirect('user:profile_detail')
        pass
    return render(request, "user/update_profile.html")
