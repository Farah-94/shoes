from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse
from store.models import Product
from cart.models import CartItem


@login_required
def cart_view(request):
    """Displays the user's cart."""
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, "cart/cart.html", {"cart_items": cart_items, "total_price": total_price})


@login_required
def add_to_cart(request, product_id):
    """Adds a product to the cart, handling size selection."""
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get("size", "M")

    # Ensure each size is stored separately per product
    cart_item, created = CartItem.objects.update_or_create(
        user=request.user,
        product=product,
        size=size,
        defaults={"quantity": 1},
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} (Size {size}) added to your cart!")
    return redirect(reverse("cart:cart_view"))


def signup(request):
    """Handles user sign-up and account creation."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
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
    """Handles user authentication."""
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
    """Handles user logout."""
    logout(request)
    messages.success(request, "You have logged out successfully!")
    return redirect("cart:signin")


class CustomLoginView(LoginView):
    """Custom login view using Django's built-in authentication."""
    template_name = "cart/signin.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse("store:index")
