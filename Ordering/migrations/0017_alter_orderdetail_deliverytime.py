# Generated by Django 3.2.5 on 2021-07-19 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ordering', '0016_auto_20210719_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='deliveryTime',
            field=models.CharField(max_length=7),
        ),
    ]