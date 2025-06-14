
from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.product_list, name="product_list"),
    path("products/<slug:slug>/", views.product_list, name="product_list_by_cat"),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),
    path("products/<int:product_id>/buy/", views.buy_product, name="buy_product"),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path("contact/", views.contact, name="contact"),
]