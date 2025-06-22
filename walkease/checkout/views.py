# walkease/checkout/views.py

import stripe
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Stripe secret key for server-side calls
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    # Pull in the user’s cart items
    from walkease.cart.models import CartItem

    cart_items  = CartItem.objects.filter(user=request.user)
    cart_total  = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'checkout/checkout.html', {
        'cart_items':        cart_items,
        'cart_total':        cart_total,
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
    })


@csrf_exempt
def create_payment_intent(request):
    try:
        # In a real app calculate dynamically!
        amount = int(request.GET.get('amount', cart_total * 100))

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='gbp',
            metadata={'integration_check': 'accept_a_payment'},
        )

        return JsonResponse({'client_secret': intent.client_secret})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
