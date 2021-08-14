# Generated by Django 3.2.5 on 2021-07-16 06:30

import Menu.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('picture', models.ImageField(upload_to=Menu.models.get_upload_path_picture)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=100)),
                ('category', models.CharField(choices=[('Starter', 'Starter'), ('Main course', 'Main course'), ('Beef', 'Beef'), ('Dessert', 'Dessert'), ('Drink', 'Drink')], max_length=11)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]