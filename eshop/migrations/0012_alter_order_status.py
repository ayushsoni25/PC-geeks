# Generated by Django 3.2.6 on 2021-09-17 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0011_alter_feedback_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Order Confirmed', 'Order Confirmed'), ('Out Of Delivery', 'Out Of Delivery'), ('Delivered', 'Delivered')], max_length=50, null=True),
        ),
    ]
