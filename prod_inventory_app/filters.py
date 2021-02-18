import django_filters
from prod_inventory_app.models import Product, Sale, Received


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['name']


class ReceivedFilter(django_filters.FilterSet):
    class Meta:
        model = Received
        fields = ['product', 'date']



class SaleFilter(django_filters.FilterSet):
    class Meta:
        model = Sale
        fields = ['product', 'date']
