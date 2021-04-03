# Generated by Django 3.1.6 on 2021-03-30 00:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod_inventory_app', '0032_auto_20210329_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='received',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='removed',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
