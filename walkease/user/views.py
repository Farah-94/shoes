from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from walkease.checkout.models import Order
 # Import Order model from checkout app
from django.contrib import messages
from .forms import ProfileUpdateForm


@login_required
def profile_detail(request):
    # For admins, show a custom admin message
    if request.user.is_superuser:
        context = {'message': "You don't have a profile because you are an admin."}
        return render(request, "user/admin_profile.html", context)

    # Retrieve the current user's order history. Orders are sorted by newest first.
    order_history = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'order_history': order_history,
    }
    return render(request, "user/profile.html", context)

@login_required
def update_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('user:profile_detail')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, "user/update_profile.html", {'form': form})