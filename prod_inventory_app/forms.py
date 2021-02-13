
from django.forms import ModelForm
from .models import *


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name','description','unit_price','total_quantity']		


class AddForm(ModelForm):
    class Meta:
        model = Restock
        fields = ['order_date','quantity_ordered','quantity_received','vendor','vendor_cost','product']


class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = ["sale_date", "product", "quantity_issued", "payment_received", "customer"]