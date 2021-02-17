import django_filters
from prod_inventory_app.models import Product, Sale, Restock


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['name']


class RestockFilter(django_filters.FilterSet):
    class Meta:
        model = Restock
        fields = ['product', 'order_date']
		
		
		
class SaleFilter(django_filters.FilterSet):
    class Meta:
        model = Sale
        fields = ['product', 'sale_date']