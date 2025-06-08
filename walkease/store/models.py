from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)  # ✅ SEO-friendly URLs

    class Meta:
        verbose_name_plural = "Categories"  # ✅ Fixed redundant `app_label`

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # ✅ Auto-generate slug from category name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  # ✅ Proper representation in Django admin


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey("store.Category", on_delete=models.CASCADE)  # ✅ Fixed circular import
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)  # Tracks stock availability
    slug = models.SlugField(unique=True, blank=True)  # Generates a URL-friendly slug
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # ✅ Tracks last modification

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # ✅ Auto-generate slug from product name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  # ✅ Proper representation in Django admin


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # ✅ Fixed nullable field
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # ✅ Tracks modifications

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity  # ✅ Auto-calculate total price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.user.username} ({self.quantity}x {self.product.name})"