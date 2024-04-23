# Generated by Django 3.2.6 on 2021-09-04 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0002_auto_20210831_1715'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='name',
        ),
        migrations.AddField(
            model_name='product',
            name='Name',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=10000),
        ),
    ]