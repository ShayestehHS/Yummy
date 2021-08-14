# Generated by Django 3.2.5 on 2021-08-04 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ordering', '0020_auto_20210804_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='deliveryDay',
            field=models.CharField(choices=[('Today', 'Today'), ('Tomorrow', 'Tomorrow')], max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='deliveryMethod',
            field=models.CharField(choices=[('Delivery', 'Delivery'), ('TakeAway', 'TakeAway')], max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='deliveryTime',
            field=models.CharField(max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='full_address',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='postal_code',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='telephone',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
