from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Ensure you have a views.py file
from .views import signup_view


app_name = "cart"


urlpatterns = [
    path("view/", views.view_cart, name="view_cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),  # Add login URL here
    path('signup/', signup_view, name='signup'),


]