# Generated by Django 3.2.6 on 2021-09-17 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0010_feedback_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='email',
            field=models.EmailField(default='', max_length=50),
        ),
    ]
