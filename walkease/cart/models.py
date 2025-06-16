from django.db import models
from django.conf import settings
from walkease.store.models import Product

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    # Remove the default value 'M'
    size = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.quantity}"
