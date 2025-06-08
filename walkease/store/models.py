from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    # Use the string "store.OrderItem" which tells Django to look for the OrderItem model
    # in the app with the label "store" (which is usually determined automatically from your AppConfig)
    items = models.ManyToManyField("store.OrderItem")
    shipping_address = models.TextField()
    payment_method = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Processing")

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(
        max_length=5,
        choices=[
            ("6", "Size 6"),
            ("7", "Size 7"),
            ("8", "Size 8"),
            ("9", "Size 9"),
            ("10", "Size 10")
        ]
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Size {self.size})"