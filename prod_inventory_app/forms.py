from django import forms
from django.forms import ModelForm
from .models import Product, Received, Sale
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput


class DateInput(forms.DateInput):
    input_type = 'date'


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description']


class ReceivedForm(ModelForm):
    class Meta:
        model = Received
        fields = ['date', 'quantity', 'vendor', 'unit_price']
        widgets = {
            'date': DateInput(),
        }


class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = ['date', 'quantity', 'payment_received', 'customer', 'unit_price']
        widgets = {
            'date': DateInput(),
        }


class SearchSalesForm(forms.ModelForm):
	start_date = forms.DateTimeField(required=False)
	end_date = forms.DateTimeField(required=False)
	class Meta:
		model = Sale
		fields = ['date', 'quantity', 'payment_received', 'customer', 'unit_price']