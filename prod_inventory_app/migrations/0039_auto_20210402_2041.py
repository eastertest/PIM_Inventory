# Generated by Django 3.1.6 on 2021-04-03 00:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prod_inventory_app', '0038_auto_20210402_2006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor', models.CharField(max_length=50, null=True, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='received',
            name='vendor1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prod_inventory_app.vendor'),
        ),
    ]
