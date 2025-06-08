from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
from walkease.store.models import Product  # ✅ Correct import

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)  # ✅ Ensures stock can't go negative
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    image = models.ImageField(upload_to="products/", null=True, blank=True)  

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(apps.get_model("store", "Product"), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=1, choices=[('S','Small'),('M','Medium'),('L','Large')])
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity  # ✅ Auto-calculated price

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through="CartItem")  # ✅ Correct relationship
    shipping_address = models.TextField()
    payment_method = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Processing")

    @property
    def calculated_total_price(self):
        return sum(item.total_price for item in self.items.all())  # ✅ Auto-calculate order total

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
