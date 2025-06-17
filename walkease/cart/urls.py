from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("view/", views.cart_view, name="view_cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("update/<int:item_id>/<str:action>/", views.update_cart, name="update_cart"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("logout/", views.logout_view, name="logout"),
]