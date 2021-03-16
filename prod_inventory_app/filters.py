from django import forms
import django_filters
from prod_inventory_app.models import Product, Sale, Received
from django.db import models


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['name']


class ReceivedFilter(django_filters.FilterSet):
    class Meta:
        model = Received
        fields = ['product', 'vendor', 'date']
        filter_overrides = {
            models.DateField: {
                'filter_class': django_filters.DateFilter,
                'extra': lambda f: {
                    'widget': forms.DateInput(attrs={'type': 'date'}),
                },
            },
        }


class SaleFilter(django_filters.FilterSet):
    class Meta:
        model = Sale
        fields = ['product', 'customer', 'date']
        filter_overrides = {
            models.DateField: {
                'filter_class': django_filters.DateFilter,
                'extra': lambda f: {
                    'widget': forms.DateInput(attrs={'type': 'date'}),
                },
            },
        }