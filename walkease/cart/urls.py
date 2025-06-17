from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = "cart"

urlpatterns = [
    path("view/", views.cart_view, name="view_cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("signup/", views.signup, name="signup"),
    # Use the built-in LoginView with your custom template.
    path("signin/", LoginView.as_view(template_name="cart/signin.html"), name="signin"),
    path("logout/", views.logout_view, name="logout"),  # if using a custom logout view
]