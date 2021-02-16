import django_filters
from prod_inventory_app.models import Product, Sale, Restock


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['name']
