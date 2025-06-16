from django.db import models
from django.conf import settings
from walkease.store.models import Product

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    size = models.CharField(max_length=10, default="M")

    class Meta:
        app_label = 'cart'  # Use the name of your app here

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.quantity}"