from django.contrib import admin

from .models import Product, Sale, Received, Removed, RemovedReason, Vendor


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'quantity', 'sales_last_thirty_days', 'sales_rate_per_day']
    ordering = ['-id']
    list_filter = ['name']


class ReceivedAdmin(admin.ModelAdmin):
    list_display = ['product', 'date', 'quantity', 'vendor1', 'unit_price']
    ordering = ['-date']
    list_filter = ['date', 'product', 'vendor1']


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


class VendorAdmin(admin.ModelAdmin):
    list_display = ['vendor']
    ordering = ['vendor']
    list_filter = ['vendor']


admin.site.register(Product, ProductAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Received, ReceivedAdmin)
admin.site.register(Removed, RemovedAdmin)
admin.site.register(RemovedReason, RemovedReasonAdmin)
admin.site.register(Vendor, VendorAdmin)

