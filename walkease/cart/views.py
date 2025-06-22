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
    # Fetch user’s cart items
    cart_items = CartItem.objects.filter(user=request.user)

    # Compute grand total
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Attach line‐item total for each cart item
    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    return render(request, "cart/cart.html", {
        "cart_items":  cart_items,
        "total_price": total_price,
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    size_value = request.POST.get("size", "M")
    # ← read the requested quantity, default to 1
    try:
        qty = int(request.POST.get("quantity", 1))
    except ValueError:
        qty = 1

    # find or create the cart item
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        size=size_value,
        defaults={"quantity": qty},
    )
    if not created:
        # if it already existed, bump by the requested amount
        cart_item.quantity += qty
        cart_item.save()

    messages.success(request, f"{product.name} added to your cart!")
    return redirect("cart:view_cart")


@login_required
def update_cart(request, item_id, action):
    """
    Updates the quantity of a given cart item.
    :param item_id: primary key of CartItem
    :param action: 'increase' or 'decrease'
    """
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    
    if action == "increase":
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Increased quantity for {cart_item.product.name}.")
    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, f"Decreased quantity for {cart_item.product.name}.")
        else:
            # If quantity reaches 1 and decreases, remove the item.
            cart_item.delete()
            messages.success(request, f"Removed {cart_item.product.name} from your cart.")
    else:
        messages.error(request, "Invalid action.")
    
    return redirect("cart:view_cart")

@login_required
def remove_from_cart(request, item_id):
    """
    Removes a product from the cart.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, f"{cart_item.product.name} removed from your cart.")
    return redirect("cart:view_cart")

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
            # Retrieve the next URL from POST data; default to the cart view.
            next_url = request.POST.get("next") or reverse("cart:view_cart")
            print("Redirecting to:", next_url)  # Debug: check redirect destination.
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    
    # For GET, retrieve the next parameter from the URL; default to cart view.
    next_url = request.GET.get("next") or reverse("cart:view_cart")
    print("Rendering sign-in with next:", next_url)  # Debug output.
    return render(request, "cart/signin.html", {"next": next_url})

def logout_view(request):
    """
    Handles user logout, shows a success message, and redirects to the sign-in page.
    """
    logout(request)
    messages.success(request, "You have logged out successfully!")
    return redirect("cart:signin")