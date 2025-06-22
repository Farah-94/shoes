import os
from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings

from .models import Product, Review


# ------------------------------------------------------------------------------
# 1) Custom ModelForm so we can include readonly image preview
# ------------------------------------------------------------------------------
# store/admin.py
class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
    image = forms.ChoiceField(choices=[
        (f, f) for f in os.listdir(
            os.path.join(settings.BASE_DIR, 'walkease/store/static/store/gallery')
        )
        if not f.startswith('.')
    ])



# ------------------------------------------------------------------------------
# 2) ProductAdmin: upload image, show thumb & preview
# ------------------------------------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    list_display    = ("name", "category", "price", "stock", "display_thumbnail")
    list_editable   = ("price", "stock")
    search_fields   = ("name", "description")
    list_filter     = ("category", "price", "stock")

    readonly_fields = ("image_preview",)
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
            "Product Image",
            {
                "fields": ("image", "image_preview"),
                "description": "Upload the main product image here.",
            },
        ),
    ]

    def display_thumbnail(self, obj):
        if obj.image and hasattr(obj.image, "url"):
            return mark_safe(
                f'<img src="{obj.image.url}" width="50" height="50" '
                f'style="object-fit:contain; border:1px solid #ccc;" />'
            )
        return "No Image"
    display_thumbnail.short_description = "Thumb"

    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, "url"):
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-height:200px; '
                f'object-fit:contain; border:1px solid #ccc;" />'
            )
        return "No Image"
    image_preview.short_description = "Preview"


# ------------------------------------------------------------------------------
# 3) ReviewAdmin: simple list display/filter/search
# ------------------------------------------------------------------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ("product", "user", "rating", "created_at")
    list_filter   = ("rating", "created_at")
    search_fields = ("comment", "user__username", "product__name")
