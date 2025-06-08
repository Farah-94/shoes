from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Ensure you have a views.py file
from .views import signup

app_name = "cart"

urlpatterns = [  
   path("view/", views.cart_view, name="view_cart"), 
   path("signup/", signup, name="signup"),
   path("login/", auth_views.LoginView.as_view(), name="login"),
   path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]