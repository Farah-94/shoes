from django.contrib import admin
from django import forms
from .models import Product 

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'price', 'stock', 'display_main_image')
    list_editable = ('price', 'stock')
    search_fields = ('name', 'description')
    list_filter = ('price', 'stock')

    def display_main_image(self, obj):
        if obj.image and obj.image.url:
            return f'<img src="{obj.image.url}" width="50">'
        return "No Image"

    display_main_image.allow_tags = True
    display_main_image.short_description = 'Main Image'

    fieldsets = [
        ('Basic Info', {
            'fields': ('name', 'price', 'stock', 'description')
        }),
        ('Product Images', {
            'fields': ('image',),
            'description': 'Upload product images.'
        }),
    ]

# Register only the Product model
admin.site.register(Product, ProductAdmin)
