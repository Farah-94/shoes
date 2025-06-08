from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse
from store.models import Product  # Import the Product model
from cart.models import CartItem  # Import the CartItem model

def cart_view(request):
    return HttpResponse("This is the cart page.")

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure new users are customers
            user.is_staff = False  
            user.is_superuser = False  
            user.save()

            # Store success message in session to persist after redirect
            request.session["signup_success"] = "Signup successful! Please log in."
            return redirect("cart:signin")  # Redirects users to sign-in page

        else:
            messages.error(request, "Signup failed! Please check your details.")

    else:
        form = UserCreationForm()

    return render(request, "cart/signup.html", {"form": form})

# Authenticate user & redirect after login
def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)  # Logs in the user without modifying roles
            return redirect("store:index")  # Redirects to homepage
        else:
            messages.error(request, "Invalid username or password. Try again.")

    return render(request, "cart/signin.html")

# Logout and redirect user
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully!")
    return redirect("cart:signin")

class CustomLoginView(LoginView):
    template_name = "cart/signin.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse("store:index")  # Ensures login redirects properly

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.update_or_create(
        user=request.user,
        product=product,
        defaults={
            "quantity": CartItem.objects.filter(user=request.user, product=product).first().quantity + 1 if not created else 1,
            "size": request.POST.get("size", "M"),
        },
    )

    messages.success(request, f"{product.name} added to your cart successfully!")
    return redirect(reverse("cart:cart"))

@login_required
def cart(request):
    # Fetch cart items for the logged-in user
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, "cart/cart.html", {"cart_items": cart_items, "total": total})