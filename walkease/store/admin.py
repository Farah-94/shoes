from django.contrib import admin
from django import forms
from .models import Product, Category

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  # ✅ No need for `image_code` dropdown anymore

class ProductInline(admin.TabularInline):
    model = Product
    extra = 1  # Allows adding 1 extra blank product per category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Shows category names
    search_fields = ('name',)  # Enables search for categories
    inlines = [ProductInline]

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'price', 'stock', 'category', 'display_main_image')
    list_editable = ('price', 'stock')  # Allow quick editing
    search_fields = ('name', 'description')
    list_filter = ('category', 'price', 'stock')

    def display_main_image(self, obj):
        if obj.image and obj.image.url:
            return f'<img src="{obj.image.url}" width="50">'  # ✅ Correct image field
        return "No Image"

    display_main_image.allow_tags = True
    display_main_image.short_description = 'Main Image'

    fieldsets = [
        ('Basic Info', {
            'fields': ('name', 'category', 'price', 'stock', 'description')
        }),
        ('Product Images', {
            'fields': ('image',),  # ✅ Using actual ImageField now
            'description': 'Upload product images.'
        }),
    ]

# Register your models here
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)