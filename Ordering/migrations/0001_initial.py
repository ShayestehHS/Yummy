# Generated by Django 3.2.5 on 2021-07-16 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('quantity', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False)),
                ('address', models.TextField()),
                ('deliveryDay', models.CharField(choices=[('Today', 'Today'), ('Tomorrow', 'Tomorrow')], default='Today', max_length=8)),
                ('deliveryTime', models.DateField(default='12:00:00')),
            ],
        ),
    ]