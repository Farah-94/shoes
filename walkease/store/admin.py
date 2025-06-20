from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from .models import Category, Product, Review

# We intentionally do NOT register the Category model 
# since we want it only to be used in the Product form. 

# Custom ModelForm for Product
class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ("name", "category", "price", "stock", "display_main_image")
    list_editable = ("price", "stock")
    search_fields = ("name", "description")
    list_filter = ("category", "price", "stock")
    fieldsets = [
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "category",
                    "price",
                    "stock",
                    "description",
                )
            },
        ),
        (
            "Product Images",
            {
                "fields": ("image",),
                "description": "Upload the main product image here.",
            },
        ),
    ]

    def display_main_image(self, obj):
        if obj.image and hasattr(obj.image, "url"):
            return mark_safe(f'<img src="{obj.image.url}" width="50" />')
        return "No Image"

    display_main_image.short_description = "Image"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("comment", "user__username", "product__name")