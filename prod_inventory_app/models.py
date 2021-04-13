from django.db import models
import datetime
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


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

    def sales_last_thirty_days(self):
        now = timezone.now()
        thirty_days_ago = now - datetime.timedelta(days=30)
        sold = Sale.objects.filter(product=self).filter(date__gte=thirty_days_ago).aggregate(Sum('quantity'))['quantity__sum']
        if sold is None:
            sold = 0
        return sold

    def sales_rate_per_day(self):
        last_thirty_days = self.sales_last_thirty_days()
        sales_rate = last_thirty_days / 30
        return sales_rate

    def inventory_zero(self):
        sales_rate = self.sales_rate_per_day()
        if sales_rate <= 0:
            return -1
        now = timezone.now()
        quantity = self.quantity()
        days_until_zero = quantity / sales_rate
        date_zero = now + datetime.timedelta(days=days_until_zero)
        return date_zero

    def year_to_date_prod(self):
        sales_ytd = Sale.objects.all().filter(date__year=2021,product=self)
        total_ytd = sum([sale.quantity * sale.unit_price for sale in sales_ytd])
        return total_ytd

    def days_left(self):
        days_left = int(self.quantity() / self.sales_rate_per_day())
        return days_left

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

    def trends():
        dates = Sale.objects.all().dates('date', 'year')
        years = [date.year for date in dates]
        perc = {}
        perc.update({years[0]:str(round(100,1))})
        for i in range(1,len(years) - 1):
            sales_base = Sale.objects.all().filter(date__year=years[i-1])
            sales_yr = Sale.objects.all().filter(date__year=years[i])
            total_base = sum([sale.quantity * sale.unit_price for sale in sales_base])
            total_yr = sum([sale.quantity * sale.unit_price for sale in sales_yr])
            trend_yr = 100 * total_yr/total_base
            perc.update({years[i]:str(round(trend_yr,1))})
        return perc

    def gross_profit():
        dates = Sale.objects.all().dates('date', 'year')
        years = [date.year for date in dates]
        gp = {}
        for i in range(0,len(years) - 1):
            sales_yr = Sale.objects.all().filter(date__year=years[i])
            total_yr = sum([sale.quantity * sale.unit_price for sale in sales_yr])
            inv_yr = Received.objects.all().filter(date__year=years[i])
            inv_cost_yr = sum([inv_prod.quantity * inv_prod.unit_price for inv_prod in inv_yr])
            gp_yr = total_yr - inv_cost_yr
            gp.update({years[i]:str(gp_yr)})
        print(gp)
        return gp

    def year_to_date_sales():
        now = timezone.now()
        year=now.year
        sales_ytd = Sale.objects.all().filter(date__year=year)
        total_ytd = sum([sale.quantity * sale.unit_price for sale in sales_ytd])
        ytd = {str(year):str(total_ytd)}
        return ytd

    def rate_of_sales_growth():
        dates = Sale.objects.all().dates('date', 'year')
        years = [date.year for date in dates]
        rosg = {}
        for i in range(1,len(years) - 1):
            sales_yr = Sale.objects.all().filter(date__year=years[i])
            sales_yr_min1 = Sale.objects.all().filter(date__year=years[i - 1])
            total_yr = sum([sale.quantity * sale.unit_price for sale in sales_yr])
            total_yr_min1 = sum([sale.quantity * sale.unit_price for sale in sales_yr_min1])
            rosg_yr = 100 * (total_yr - total_yr_min1) / total_yr_min1
            rosg.update({years[i]:str(round(rosg_yr,2))})
        return rosg

    def __str__(self):
        return self.product.name + " " + str(self.date)


class Vendor(models.Model):
    vendor = models.CharField(max_length=50, null=True, unique=True)

    def save(self, *args, **kwargs):
        self.vendor = self.vendor.lower()
        return super(Vendor, self).save(*args, **kwargs)

    def __str__(self):
        return self.vendor


class Received(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    vendor1 = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, verbose_name='Vendor')
    unit_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def __str__(self):
        return self.product.name

class RemovedReason(models.Model):
    reason = models.CharField(max_length=200, null=True, unique=True)

    def save(self, *args, **kwargs):
        self.reason = self.reason.lower()
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
