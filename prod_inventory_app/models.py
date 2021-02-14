from django.db import models
from django.utils import timezone
import datetime


class Product(models.Model):
    name = models.CharField(max_length = 50, null = True, blank = True)
    description = models.CharField(max_length = 50, null = True, blank = True)
    unit_price = models.DecimalField(default = 0, decimal_places = 2, max_digits = 10, null = True, blank = True)
    total_quantity = models.IntegerField(default = 0, null = True, blank = True)

    def __str__(self):
        return self.name


class Sale(models.Model):
    sale_date =  models.DateField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    customer = models.CharField(max_length = 50, null = True, blank = True)
    quantity_issued = models.IntegerField(default = 0, null = True, blank = True)
    unit_price = models.DecimalField(default = 0, decimal_places = 2,  max_digits = 10, null = True, blank = True)
    payment_received = models.DecimalField(default = 0, decimal_places = 2,  max_digits = 10, null = True, blank = True)

    def get_total(self):
        total = self.quantity_issued * self.unit_price
        return (total)

    def get_change(self):
        change = self.get_total() - self.payment_received
        return (change)

    def __str__(self):
        return self.product.name


class Restock(models.Model):
    order_date = models.DateField(default=datetime.date.today)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity_ordered = models.IntegerField(default = 0, null = True, blank = True)
    quantity_received = models.IntegerField(default = 0, null = True, blank = True)
    vendor = models.CharField(max_length = 50, null = True, blank = True)
    vendor_cost = models.DecimalField(default = 0, decimal_places = 2,  max_digits = 10, null = True, blank = True)

