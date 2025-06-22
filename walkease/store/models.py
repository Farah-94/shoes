from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    # … your existing Category methods …

class Product(models.Model):
    category    = models.ForeignKey(
                      Category,
                      related_name="products",
                      on_delete=models.PROTECT,
                      null=True,
                      blank=True,
                  )
    name        = models.CharField(max_length=255)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock       = models.PositiveIntegerField(default=0)

    # ← Replace ImageField with CharField for static filenames
    image = models.CharField(
        max_length=255,
        blank=True,
        help_text="Filename in store/gallery, e.g. 'crocs.jpg'"
    )

    def __str__(self):
        return self.name
    


    

class Review(models.Model):
    RATING_CHOICES = [(i, f"{i} Star{'' if i == 1 else 's'}") for i in range(1, 6)]

    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user       = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)
    rating     = models.IntegerField(choices=RATING_CHOICES)
    comment    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"{self.product.name} – {self.rating} by {username}"


class OrderItem(models.Model):
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size     = models.CharField(
                   max_length=5,
                   choices=[(str(i), f"Size {i}") for i in range(6, 11)]
               )

    def __str__(self):
        return f"{self.quantity}× {self.product.name} (Size {self.size})"


class Order(models.Model):
    user             = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    items            = models.ManyToManyField(OrderItem)
    shipping_address = models.TextField()
    payment_method   = models.CharField(max_length=50)
    total_price      = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status           = models.CharField(max_length=20, default="Processing")
    created_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} – {self.user.username}"
