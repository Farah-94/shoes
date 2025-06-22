# walkease/checkout/urls.py
from django.urls import path
from . import views

app_name = "checkout"

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("create-payment-intent/", views.create_payment_intent, name="create_payment_intent"),
    path("success/", views.order_success, name="success"),
]
