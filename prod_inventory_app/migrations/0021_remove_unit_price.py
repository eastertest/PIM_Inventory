# Generated by Django 3.1.6 on 2021-03-20 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod_inventory_app', '0020_auto_20210319_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='remove',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]