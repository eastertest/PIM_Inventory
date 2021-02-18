from django.forms import ModelForm
from .models import *


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description']


class ReceivedForm(ModelForm):
    class Meta:
        model = Received
        fields = ['date', 'quantity', 'vendor', 'unit_price']


class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = ['date', 'quantity', 'payment_received', 'customer', 'unit_price']
