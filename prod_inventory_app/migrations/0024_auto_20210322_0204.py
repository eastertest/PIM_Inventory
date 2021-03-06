# Generated by Django 3.1.6 on 2021-03-22 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod_inventory_app', '0023_auto_20210322_0101'),
    ]

    operations = [
        migrations.RenameField(
            model_name='remove',
            old_name='vendor',
            new_name='customer',
        ),
        migrations.AddField(
            model_name='remove',
            name='payment_received',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='remove',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='remove',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
