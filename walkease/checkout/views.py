# walkease/checkout/views.py

import stripe
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from walkease.cart.models import CartItem

# Configure Stripe with your secret key
stripe.api_key = settings.STRIPE_SECRET_KEY


from django.shortcuts import render

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_total = sum(i.product.price * i.quantity for i in cart_items)

    # Build the full URL Stripe requires:
    success_url = request.build_absolute_uri(
        reverse('checkout:success')            # -> "/checkout/success/"
    )                                          # -> "https://walkease-app-…/checkout/success/"

    return render(request, "checkout/checkout.html", {
        "cart_items":         cart_items,
        "cart_total":         cart_total,
        "stripe_public_key":  settings.STRIPE_PUBLIC_KEY,
        "payment_success_url": success_url,      # ← pass it into the template
    })

@login_required
@csrf_exempt
def create_payment_intent(request):
    """
    Creates a Stripe PaymentIntent for the user’s current cart total.
    Returns the client_secret for the frontend to confirm payment.
    """
    # Re-fetch cart items and total
    cart_items = CartItem.objects.filter(user=request.user)
    cart_total = sum(item.product.price * item.quantity for item in cart_items)

    # Stripe expects amount in the smallest currency unit (pence)
    amount = int(cart_total * 100)

    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='gbp',
            metadata={
                'integration_check': 'accept_a_payment',
                'user_id': str(request.user.id)
            },
        )
        return JsonResponse({'client_secret': intent.client_secret})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def order_success(request):
    # You can pull in any order info here (from session, DB, etc.)
    return render(request, "checkout/order_success.html")