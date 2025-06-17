from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from walkease.store.models import Product
from walkease.cart.models import CartItem

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
    If the user is not signed in, they will be redirected to sign in.
    After sign in, they are redirected back to view their cart.
    """
    product = get_object_or_404(Product, id=product_id)
    # Retrieve size from POST; default to "M" if not provided.
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
    return redirect(reverse("cart:view_cart"))

def signup(request):
    """
    Handles user sign-up and account creation using Django's built-in UserCreationForm.
    On successful signup, a session message is set and the user is redirected to sign in.
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
    Custom sign-in view.
    It checks for the 'next' parameter to redirect the user to their desired page after a successful login.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            # Retrieve the next URL from the form data; default to the cart view.
            next_url = request.POST.get("next") or reverse("cart:view_cart")
            # Debug: Uncomment the following line if you need to check the next_url value.
            # print("Redirecting to:", next_url)
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")

    # For GET, retrieve the next parameter from the URL, defaulting to the cart view.
    next_url = request.GET.get("next") or reverse("cart:view_cart")
    # Debug: Uncomment the following line if you need to check the next_url value.
    # print("Rendering sign-in with next:", next_url)
    return render(request, "cart/signin.html", {"next": next_url})

def logout_view(request):
    """
    Handles user logout, shows a success message, and redirects to the sign-in page.
    """
    logout(request)
    messages.success(request, "You have logged out successfully!")
    return redirect("cart:signin")