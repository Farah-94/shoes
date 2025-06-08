from django.apps import apps  # ✅ Import apps for dynamic model loading
from django.db import models

class CartItem(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE)  # ✅ Use string reference instead of direct import
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
