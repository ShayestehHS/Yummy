# Generated by Django 3.2.5 on 2021-08-03 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_remove_user_is_subscriber'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driver',
            old_name='User',
            new_name='user',
        ),
    ]
