from django.contrib import admin

from .models import Product, ProductType
# Register your models here.

class ProductTypeInline(admin.TabularInline):
    """Puts a product's type as an inline for admin."""
    model = ProductType

class ProductInline(admin.TabularInline):
    """Puts a product as an inline for admin."""
    model = Product

class ProductAdmin(admin.ModelAdmin):
    """Lists all products and their contents."""
    model = Product

class ProductTypeAdmin(admin.ModelAdmin):
    """Lists all product types and products categorized as that type."""
    model = ProductType
    inlines = [ProductInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
