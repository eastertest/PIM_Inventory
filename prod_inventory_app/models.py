from django.db import models
from django.utils import timezone
import datetime
from django.db.models import Sum


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True, blank=True)

    def quantity(self):
        received = Received.objects.filter(product=self).aggregate(Sum('quantity'))['quantity__sum']
        if received == None:
            received = 0;
        sold = Sale.objects.filter(product=self).aggregate(Sum('quantity'))['quantity__sum']
        if sold == None:
            sold = 0;
        return received - sold

    def __str__(self):
        return self.name


class Sale(models.Model):
    date = models.DateField(default=datetime.date.today)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    payment_received = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def get_total(self):
        total = self.quantity * self.unit_price
        return (total)

    def get_change(self):
        change = self.get_total() - self.payment_received
        return (change)

    def __str__(self):
        return self.product.name


class Received(models.Model):
    date = models.DateField(default=datetime.date.today)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    vendor = models.CharField(max_length=50, null=True, blank=True)
    unit_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def __str__(self):
        return self.product.name
