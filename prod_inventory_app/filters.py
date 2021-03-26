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
    start_date = django_filters.DateFilter(field_name='date',lookup_expr=('lte'), widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = django_filters.DateFilter(field_name='date',lookup_expr=('gte'), widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Sale
        fields = ['product', 'customer', 'start_date', 'end_date']
        filter_overrides = {
            models.DateField: {
                'filter_class': django_filters.DateFilter,
                'extra': lambda f: {
                    'widget': forms.DateInput(attrs={'type': 'date'}),
                },
            },
        }
