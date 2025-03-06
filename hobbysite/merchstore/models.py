from django.db import models
from django.urls import reverse

# Create your models here.

class ProductType(models.Model):
    """A model representing a product type or category."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'product_type'
        verbose_name_plural = 'product_types'

class Product(models.Model):
    """A model representing a product"""
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2)
    product_type = models.ForeignKey(ProductType,
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     related_name='product')

    class Meta:
        ordering = ['name']
        verbose_name = 'product'
        verbose_name_plural = 'products'
