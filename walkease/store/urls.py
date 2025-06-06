from django.urls import path
from .views import index, product_list, buy_product

app_name = 'store'  # This sets a namespace for your store app URLs

urlpatterns = [
    path('', index, name='index'),
    path('products/', product_list, name='productlist'),
    path('buy/<int:product_id>/', buy_product, name='buy_product'),
]