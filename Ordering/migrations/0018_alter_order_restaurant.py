# Generated by Django 3.2.5 on 2021-08-03 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Yummy', '0005_alter_restaurantreview_user'),
        ('Ordering', '0017_alter_orderdetail_deliverytime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Yummy.restaurant'),
        ),
    ]