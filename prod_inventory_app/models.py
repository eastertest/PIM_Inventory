from django.db import models
import datetime
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Product, self).save(*args, **kwargs)

    def quantity(self):
        received = Received.objects.filter(product=self).aggregate(Sum('quantity'))['quantity__sum']
        if received is None:
            received = 0
        sold = Sale.objects.filter(product=self).aggregate(Sum('quantity'))['quantity__sum']
        if sold is None:
            sold = 0
        removed = Removed.objects.filter(product=self).aggregate(Sum('quantity'))['quantity__sum']
        if removed is None:
            removed = 0
        return received - sold - removed

    def quantityovertime(self, date):
        received = Received.objects.filter(product=self).filter(date__lte=date).aggregate(Sum('quantity'))['quantity__sum']
        if received is None:
            received = 0
        sold = Sale.objects.filter(product=self).filter(date__lte=date).aggregate(Sum('quantity'))['quantity__sum']
        if sold is None:
            sold = 0
        removed = Removed.objects.filter(product=self).filter(date__lte=date).aggregate(Sum('quantity'))['quantity__sum']
        if removed is None:
            removed = 0
        return received - sold - removed

    def __str__(self):
        return self.name


class Sale(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
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
    date = models.DateTimeField(default=datetime.datetime.now)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    vendor = models.CharField(max_length=50, null=True, blank=True)
    unit_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def __str__(self):
        return self.product.name

class RemovedReason(models.Model):
    reason = models.CharField(max_length=200, null=True, unique=True)

    def save(self, *args, **kwargs):
        self.reason = self.name.lower()
        return super(RemovedReason, self).save(*args, **kwargs)

    def __str__(self):
        return self.reason


class Removed(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    reason1 = models.ForeignKey(RemovedReason, on_delete=models.CASCADE, null=True, verbose_name='Reason')

    def __str__(self):
        return self.product.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
