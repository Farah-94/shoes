# walkease/checkout/urls.py
from django.urls import path, include
from . import views  # Make sure that you have a views.py in walkease/checkout
from .views import create_payment_intent

app_name = "checkout"

urlpatterns = [
  path("", views.checkout, name="checkout"),
  path("create-payment-intent/", views.create_payment_intent, name="create-payment-intent"),
]
