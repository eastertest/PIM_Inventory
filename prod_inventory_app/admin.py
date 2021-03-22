from django.contrib import admin

from .models import Product, Sale, Received


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'quantity')


class ReceivedAdmin(admin.ModelAdmin):
    list_display = ('product', 'date', 'quantity', 'vendor', 'unit_price')


class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'date', 'customer', 'quantity', 'unit_price')




admin.site.register(Product, ProductAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Received, ReceivedAdmin)

