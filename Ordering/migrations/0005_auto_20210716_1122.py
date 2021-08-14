# Generated by Django 3.2.5 on 2021-07-16 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ordering', '0004_auto_20210716_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deliveryDay',
            field=models.CharField(choices=[('Today', 'Today'), ('Tomorrow', 'Tomorrow')], max_length=8),
        ),
        migrations.AlterField(
            model_name='order',
            name='deliveryMethod',
            field=models.CharField(max_length=8),
        ),
    ]