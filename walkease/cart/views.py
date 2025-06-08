from pyexpat.errors import messages
from django.shortcuts import redirect, render, get_object_or_404

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
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

            # ✅ Ensure new users are customers
            user.is_staff = False  
            user.is_superuser = False  
            user.save()

            messages.success(request, "Signup successful! Please log in.")
            return redirect("store:signin")  # ✅ Redirects users to sign-in page

        else:
            messages.error(request, "Signup failed! Please check your details.")  # ✅ Show error message

    else:
        form = UserCreationForm()

    return render(request, "store/signup.html", {"form": form})


# ✅ SIGNIN: Authenticate user & redirect after login
def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)  # ✅ Logs in the user without modifying roles
            return redirect("store:index")  # ✅ Redirects to homepage (ensure this exists in urls.py)
        else:
            messages.error(request, "Invalid username or password. Try again.")

    return render(request, "store/signin.html")  # ✅ Reloads sign-in page to show errors

# ✅ LOGOUT: Ends session & redirects user
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully!")
    return redirect("store:signin")

class CustomLoginView(LoginView):
    template_name = "store/signin.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse("index")  # ✅ Ensures login redirects to homepage

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please sign in to view your cart.")  # ✅ Add warning message
        return redirect(f"{reverse('store:signin')}?next={reverse('store:cart')}")  # ✅ Redirects to sign-in & then to cart
    
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={
            "quantity": 1,
            "size": request.POST.get("size", "M"),
        },
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to your cart successfully!")
    return redirect(reverse("store:cart"))





@login_required
def cart(request):
    # Redirect user to sign-in page if they are not authenticated
    if not request.user.is_authenticated:
        messages.warning(request, "Please sign in to view your cart.")
        return redirect("store:signin")

    # Fetch cart items for the logged-in user
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, "store/cart.html", {"cart_items": cart_items, "total": total})
