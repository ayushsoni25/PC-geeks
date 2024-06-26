# Generated by Django 3.2.6 on 2021-09-15 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0005_auto_20210905_1638'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='customer_order',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='mobile_no',
            new_name='mobile',
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.CharField(max_length=20),
        ),
    ]
