# walkease/checkout/views.py

import stripe
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from walkease.cart.models import CartItem

# Configure Stripe with your secret key
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    """
    Renders the checkout page with the user’s cart items,
    cart total, and the Stripe public key for client-side.
    """
    cart_items = CartItem.objects.filter(user=request.user)
    cart_total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'checkout/checkout.html', {
        'cart_items':        cart_items,
        'cart_total':        cart_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
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
