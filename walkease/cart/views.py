# walkease/cart/views.py

from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from walkease.store.models import Product
from walkease.cart.models import CartItem

# import Allauth’s views
from allauth.account.views import LoginView, LogoutView


@login_required
def cart_view(request):
    """Show the user’s cart with line‐item and grand totals."""
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    return render(request, "cart/cart.html", {
        "cart_items":  cart_items,
        "total_price": total_price,
    })


@login_required
def add_to_cart(request, product_id):
    """Add a product to the cart, or bump quantity if it already exists."""
    product = get_object_or_404(Product, id=product_id)
    size_value = request.POST.get("size", "M")
    try:
        qty = int(request.POST.get("quantity", 1))
    except ValueError:
        qty = 1

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        size=size_value,
        defaults={"quantity": qty},
    )
    if not created:
        cart_item.quantity += qty
        cart_item.save()

    messages.success(request, f"{product.name} added to your cart!")
    return redirect("cart:view_cart")


@login_required
def update_cart(request, item_id, action):
    """
    Increase or decrease a cart item’s quantity, or remove it if quantity hits zero.
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
            cart_item.delete()
            messages.success(request, f"Removed {cart_item.product.name} from your cart.")
    else:
        messages.error(request, "Invalid action.")

    return redirect("cart:view_cart")


@login_required
def remove_from_cart(request, item_id):
    """Remove a product from the cart entirely."""
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, f"{cart_item.product.name} removed from your cart.")
    return redirect("cart:view_cart")


def cart_login_view(request, *args, **kwargs):
    """
    Delegate to Allauth’s LoginView but render cart/signin.html.
    """
    view = LoginView.as_view(template_name="cart/signin.html")
    return view(request, *args, **kwargs)


def cart_logout_view(request, *args, **kwargs):
    """
    Delegate to Allauth’s LogoutView but render cart/signout.html.
    """
    view = LogoutView.as_view(template_name="cart/signout.html")
    return view(request, *args, **kwargs)
