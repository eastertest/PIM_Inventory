# Generated by Django 3.1.6 on 2021-02-11 16:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('total_quantity', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_date', models.DateField(blank=True, null=True)),
                ('customer', models.CharField(blank=True, max_length=50, null=True)),
                ('quantity_issued', models.IntegerField(blank=True, default=0, null=True)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prod_inventory_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='Restock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(default=datetime.date.today)),
                ('quantity_ordered', models.IntegerField(blank=True, default=0, null=True)),
                ('quantity_received', models.IntegerField(blank=True, default=0, null=True)),
                ('vendor', models.CharField(blank=True, max_length=50, null=True)),
                ('vendor_cost', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prod_inventory_app.product')),
            ],
        ),
    ]
