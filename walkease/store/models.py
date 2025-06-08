from django.db import models





from django.db import models

class Product(models.Model):
    class Meta:
        app_label = "store"  # ✅ Explicitly set the app label

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", null=True, blank=True)

    def __str__(self):
        return self.name



class Order(models.Model):
    class Meta:
        app_label = "store"  # ✅ Explicit app label prevents conflicting models

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    items = models.ManyToManyField("cart.CartItem")  # ✅ Referencing by string
    shipping_address = models.TextField()
    payment_method = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Processing")

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
