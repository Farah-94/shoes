from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse
from walkease.store.models import Product  # Ensures correct model reference
from walkease.cart.models import CartItem  # Fully qualified path for CartItem

@login_required
def cart_view(request):
    """
    Displays the user's cart.
    Retrieves all cart items for the user and calculates the total price.
    """
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, "cart/cart.html", {"cart_items": cart_items, "total_price": total_price})

@login_required
def add_to_cart(request, product_id):
    """
    Adds a product to the cart.
    Uses update_or_create to increment quantity if the item already exists.
    """
    product = get_object_or_404(Product, id=product_id)

    # Retrieve size from POST; default to "M" if no size is provided.
    size_value = request.POST.get("size", "M")

    cart_item, created = CartItem.objects.update_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": 1, "size": size_value},
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to your cart!")
    return redirect(reverse("cart:cart_view"))


def signup(request):
    """
    Handles user sign-up and account creation using Django's built-in UserCreationForm.
    On successful signup, sets a session message and redirects to the sign-in page.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure no admin privileges are granted on signup.
            user.is_staff = False
            user.is_superuser = False
            user.save()

            request.session["signup_success"] = "Signup successful! Please log in."
            return redirect("cart:signin")
        else:
            messages.error(request, "Signup failed! Please check your details.")
    else:
        form = UserCreationForm()

    return render(request, "cart/signup.html", {"form": form})

def signin(request):
    """
    Handles user authentication.
    On valid credentials, logs in the user and redirects to the store index.
    Otherwise, displays an error message.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("store:index")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "cart/signin.html")

def logout_view(request):
    """
    Handles user logout, shows a success message, and redirects to the sign-in page.
    """
    logout(request)
    messages.success(request, "You have logged out successfully!")
    return redirect("cart:signin")

class CustomLoginView(LoginView):
    """
    Custom login view that uses the template in cart/signin.html.
    Redirects authenticated users and directs successful logins to the store index.
    """
    template_name = "cart/signin.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse("store:index")
    