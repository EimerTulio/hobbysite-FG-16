from django.db import models
from django.urls import reverse
from user_management.models import Profile

# Create your models here.

class ProductType(models.Model):
    """A model representing a product type or category."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Product type'
        verbose_name_plural = 'Product types'

class Product(models.Model):
    """A model representing a product"""
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=13, decimal_places=2)
    product_type = models.ForeignKey(ProductType,
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     related_name='product')
    owner = models.ForeignKey(Profile,
                              on_delete=models.CASCADE,
                              default=None,
                              related_name='product')
    stock = models.PositiveBigIntegerField(default=1)

    STATUS_CHOICES = {
        "A": "Available",
        "S": "On sale",
        "O": "Out of stock",
    }
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICES,
                              default="A",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('merchstore:merch-detail', args=[self.pk])

    def get_update_url(self):
        return reverse('merchstore:merch-update', args=[self.pk])

    class Meta:
        ordering = ['owner', 'name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

class Transaction(models.Model):
    buyer = models.ForeignKey(Profile,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 default=None,
                                 related_name='transactions')
    product = models.ForeignKey(Product,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='transactions')
    amount = models.PositiveIntegerField(default=1)

    STATUS_CHOICES = {
        "C": "On cart",
        "P": "To pay",
        "S": "To ship",
        "R": "To receive",
        "D": "Delivered",
    }
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICES,
                              default="C")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.buyer.name + " " + self.product.name + "x" + str(self.amount) + " on " + str(self.created_on)
