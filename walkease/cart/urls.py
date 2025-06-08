from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Ensure you have a views.py file
from .views import signup_view

urlpatterns = [
    path('', views.cart_view, name='cart-home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Add login URL here
    path('signup/', signup_view, name='signup'),


]