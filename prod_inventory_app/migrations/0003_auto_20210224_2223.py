# Generated by Django 3.1.6 on 2021-02-25 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod_inventory_app', '0002_chart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chart',
            name='product',
        ),
        migrations.AddField(
            model_name='chart',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]