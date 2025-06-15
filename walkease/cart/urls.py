from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # This imports from walkease/cart/views.py

app_name = "cart"

urlpatterns = [  
    path("view/", views.cart_view, name="view_cart"),
path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),  
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]