# Generated by Django 3.1.6 on 2021-04-03 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prod_inventory_app', '0039_auto_20210402_2041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='received',
            name='vendor',
        ),
        migrations.AlterField(
            model_name='received',
            name='vendor1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prod_inventory_app.vendor', verbose_name='Vendor'),
        ),
    ]
