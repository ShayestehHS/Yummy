# Generated by Django 3.2.5 on 2021-07-16 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ordering', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deliveryTime',
            field=models.DateField(),
        ),
    ]
