from django.contrib import admin

from .models import Product, Sale, Received, Removed, RemovedReason


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'quantity']
    ordering = ['-id']
    list_filter = ['name']


class ReceivedAdmin(admin.ModelAdmin):
    list_display = ['product', 'date', 'quantity', 'vendor', 'unit_price']
    ordering = ['-date']
    list_filter = ['date', 'product']


class SaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'date', 'customer', 'quantity', 'unit_price']
    ordering = ['-date']
    list_filter = ['date', 'product']


class RemovedAdmin(admin.ModelAdmin):
    list_display = ['product', 'date', 'quantity', 'reason1']
    ordering = ['-date']
    list_filter = ['date', 'product', 'reason1']


class RemovedReasonAdmin(admin.ModelAdmin):
    list_display = ['reason']
    ordering = ['reason']
    list_filter = ['reason']



admin.site.register(Product, ProductAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Received, ReceivedAdmin)
admin.site.register(Removed, RemovedAdmin)
admin.site.register(RemovedReason, RemovedReasonAdmin)

