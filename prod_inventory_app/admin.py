from django.contrib import admin

from .models import Product, Sale, Restock


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'total_quantity','quantity')


class RestockAdmin(admin.ModelAdmin):
    list_display = ('product', 'order_date', 'quantity_ordered', 'quantity_received', 'vendor', 'vendor_cost')


admin.site.register(Product, ProductAdmin)
admin.site.register(Sale)
admin.site.register(Restock, RestockAdmin)
