# walkease/checkout/urls.py
from django.urls import path
from . import views  # Make sure that you have a views.py in walkease/checkout

urlpatterns = [
    path('', views.index, name='checkout-index'),
]