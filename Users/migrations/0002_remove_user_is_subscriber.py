# Generated by Django 3.2.5 on 2021-08-01 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_subscriber',
        ),
    ]
