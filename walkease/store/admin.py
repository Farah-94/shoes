import os
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.templatetags.static import static
from django.conf import settings

from .models import Product, Review


# ------------------------------------------------------------------------------
# 1) Custom ModelForm: dropdown of filenames from your static gallery folder
# ------------------------------------------------------------------------------
class ProductAdminForm(forms.ModelForm):
    image = forms.ChoiceField(
        choices=[],
        required=False,
        label="Image filename from store/gallery"
    )

    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        gallery_dir = os.path.join(
            settings.BASE_DIR,
            "walkease", "store", "static", "store", "gallery"
        )
        files = []
        if os.path.isdir(gallery_dir):
            for fname in sorted(os.listdir(gallery_dir)):
                path = os.path.join(gallery_dir, fname)
                if os.path.isfile(path) and not fname.startswith("."):
                    files.append((fname, fname))

        # prepend blank choice
        self.fields["image"].choices = [("", "---------")] + files


# ------------------------------------------------------------------------------
# 2) ProductAdmin: show thumbnails, preview & use dropdown field
# ------------------------------------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    list_display  = ("name", "category", "price", "stock", "thumbnail")
    list_editable = ("price", "stock")
    search_fields = ("name", "description")
    list_filter   = ("category", "price", "stock")

    readonly_fields = ("image_preview",)
    fieldsets = [
        ("Basic Info", {
            "fields": ("name", "category", "price", "stock", "description")
        }),
        ("Product Image", {
            "fields": ("image", "image_preview"),
            "description": "Pick a filename from store/static/store/gallery/",
        }),
    ]

    def thumbnail(self, obj):
        if obj.image:
            url = static(f"store/gallery/{obj.image}")
            return format_html(
                '<img src="{}" width="50" height="50" '
                'style="object-fit:contain; border:1px solid #ccc" />',
                url
            )
        return "(No image)"
    thumbnail.short_description = "Thumb"

    def image_preview(self, obj):
        if obj.image:
            url = static(f"store/gallery/{obj.image}")
            return format_html(
                '<img src="{}" style="max-height:200px; '
                'object-fit:contain; border:1px solid #ccc;" />',
                url
            )
        return "(No image)"
    image_preview.short_description = "Preview"


# ------------------------------------------------------------------------------
# 3) ReviewAdmin: unchanged
# ------------------------------------------------------------------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ("product", "user", "rating", "created_at")
    list_filter   = ("rating", "created_at")
    search_fields = ("comment", "user__username", "product__name")
