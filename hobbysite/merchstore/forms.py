from django import forms

from .models import Product, Transaction


class TransactionForm(forms.ModelForm):
    """A form for transactions."""
    class Meta:
        model = Transaction
        fields = ['amount']

    product = Product()

    def set_product(self, transaction_product):
        """Sets the product the TransactionForm is for."""
        self.product = transaction_product

    def clean(self):
        """Stops the user from ordering more than the available amount."""
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        stock = self.product.stock
        if amount > stock:
            raise forms.ValidationError("Not enough stock for this order!")

        return cleaned_data


class ProductForm(forms.ModelForm):
    """A form for products."""
    class Meta:
        model = Product
        exclude = ['owner']

    def update_status(self):
        """Sets status to out of stock when there is no stock."""
        stock = self.cleaned_data['stock']
        status = self.cleaned_data['status']
        if stock <= 0:
            status = 'O'
        return status

    def update_stock(self):
        """Sets stock to 0 when status says out of stock."""
        stock = self.cleaned_data['stock']
        status = self.cleaned_data['status']
        if status == 'O':
            stock = 0
        return stock
