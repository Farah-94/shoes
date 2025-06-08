from django.db import models
from django.contrib.auth.models import User
from django.apps import apps

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(apps.get_model("store", "Product"), on_delete=models.CASCADE)  # ✅ Dynamic loading
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
