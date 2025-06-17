import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Set your secret key for Stripe API calls
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt  # In production, secure this endpoint appropriately
def create_payment_intent(request):
    try:
        # For demonstration, the amount is hardcoded to 1000 pence (£10.00)
        amount = 1000  # Calculate dynamically in a real app

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='gbp',  # Set currency to British Pounds
            metadata={'integration_check': 'accept_a_payment'},
        )

        return JsonResponse({
            'client_secret': intent.client_secret,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)