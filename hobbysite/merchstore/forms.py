from django import forms

from .models import Product, Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['owner']

    def update_status(self):
        stock = self.cleaned_data['stock']
        status = self.cleaned_data['status']
        if stock <= 0:
            status = 'O'
        return status

    def update_stock(self):
        stock = self.cleaned_data['stock']
        status = self.cleaned_data['status']
        if status == 'O':
            stock = 0
        return stock
