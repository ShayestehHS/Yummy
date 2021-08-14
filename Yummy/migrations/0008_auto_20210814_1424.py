# Generated by Django 3.2.5 on 2021-08-14 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Yummy', '0007_alter_restaurant_delivery_charge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='city',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='is_submit',
            field=models.BooleanField(default=False, help_text='Only superusers can submit.'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='name',
            field=models.CharField(help_text='Maximum length is 40', max_length=40, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='restaurantreview',
            name='courtesy',
            field=models.DecimalField(decimal_places=3, help_text='Maximum number is 9999.999', max_digits=4),
        ),
        migrations.AlterField(
            model_name='restaurantreview',
            name='description',
            field=models.TextField(help_text='Maximum length is 200', max_length=200),
        ),
        migrations.AlterField(
            model_name='restaurantreview',
            name='food_quality',
            field=models.DecimalField(decimal_places=3, help_text='Maximum number is 9999.999', max_digits=4),
        ),
        migrations.AlterField(
            model_name='restaurantreview',
            name='price',
            field=models.DecimalField(decimal_places=3, help_text='Maximum number is 9999.999', max_digits=4),
        ),
        migrations.AlterField(
            model_name='restaurantreview',
            name='punctuality',
            field=models.DecimalField(decimal_places=3, help_text='Maximum number is 9999.999', max_digits=4),
        ),
    ]
