# Generated by Django 3.1.6 on 2021-04-02 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prod_inventory_app', '0036_auto_20210402_1943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='removed',
            name='reason',
        ),
    ]