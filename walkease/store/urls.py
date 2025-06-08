from django.urls import path
from . import views  # ✅ Simplified import

app_name = "store"  # ✅ Ensures namespace for URL resolution

urlpatterns = [
    path("", views.index, name="index"),  # Homepage
    path("products/", views.product_list, name="productlist"),  # Product list
    path("buy/<int:product_id>/", views.buy_product, name="buy_product"),  # Purchase functionality
]
