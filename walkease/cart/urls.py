# walkease/cart/urls.py

from django.urls import path
from allauth.account import views as a_views
from . import views  # your cart_view, add_to_cart, etc.
from django.contrib.auth.views import LogoutView as DjangoLogoutView

app_name = "cart"

urlpatterns = [
    path("view/", views.cart_view, name="view_cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("update/<int:item_id>/<str:action>/", views.update_cart, name="update_cart"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),

    # ————————————————
    # hook Allauth here for signup / signin / signout
    # ————————————————
    path(
        "signup/",
        a_views.SignupView.as_view(template_name="cart/signup.html"),
        name="account_signup",       # must be account_signup
    ),
    path(
        "signin/",
        a_views.LoginView.as_view(template_name="cart/signin.html"),
        name="account_login",        # must be account_login
    ),
    path(
    "logout/",
      DjangoLogoutView.as_view(
      template_name="cart/signout.html",
      next_page="cart:account_login"      # ← redirect here after GET
    ),
    name="account_logout",
  ),
]
