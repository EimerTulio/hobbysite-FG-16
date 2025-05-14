from django.contrib import admin

from .models import Product, ProductType
# Register your models here.

class ProductInline(admin.TabularInline):
    """Puts a product as an inline for admin."""
    model = Product
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    """Lists all products and their contents."""
    model = Product

    list_display = ['name', 'price', 'status', 'stock', 'product_type', 'owner']
    list_filter = ['product_type', ]
    list_editable = ['price', 'product_type', 'stock', 'status']
    ordering = ['name', 'product_type', 'price',]
    search_fields = ['name',]
    autocomplete_fields = ['product_type',]


class ProductTypeAdmin(admin.ModelAdmin):
    """Lists all product types and products categorized as that type."""
    model = ProductType
    inlines = [ProductInline,]
    ordering = ['name',]
    search_fields = ['name',]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
