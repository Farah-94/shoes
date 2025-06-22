# walkease/store/models.py

import os
from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


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

    # Primary image filename (fallback if no inline images are set)
    image = models.CharField(
        max_length=255,
        blank=True,
        default='default.jpg',          # ← add this
        help_text="Main filename in store/gallery/, e.g. 'crocs_front.jpg'"
    )

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE
    )
    filename = models.FilePathField(
        path=os.path.join(
            settings.BASE_DIR,
            "walkease", "store", "static", "store", "gallery"
        ),
        match=r".*\.(jpg|jpeg|png|gif)$",
        recursive=False,
        blank=True,
        help_text="Select a file from store/static/store/gallery/"
    )

    def __str__(self):
        # show only the basename, not full path
        return f"{self.product.name} → {os.path.basename(self.filename)}"


class Review(models.Model):
    RATING_CHOICES = [(i, f"{i} Star{'' if i == 1 else 's'}") for i in range(1, 6)]

    product    = models.ForeignKey(
                     Product,
                     on_delete=models.CASCADE,
                     related_name="reviews"
                 )
    user       = models.ForeignKey(
                     settings.AUTH_USER_MODEL,
                     on_delete=models.SET_NULL,
                     null=True,
                     blank=True
                 )
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
