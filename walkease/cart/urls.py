from django.urls import path
from . import views  # Make sure you have a views.py file in the cart app

urlpatterns = [
    path('', views.cart_view, name='cart-home'),
]