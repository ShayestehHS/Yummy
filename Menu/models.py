import os

from django.core.exceptions import ValidationError
from django.db import models

from Yummy.models import Restaurant
from utility.Compress import compress_image


def get_upload_path_picture(instance, filename):
    return os.path.join('Restaurant', f'{instance.menu.restaurant.name}',
                        'Menu', f'{instance.category}', filename)


def custom_image_validator(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path filename
    valid = ['.jpg', '.png']
    if ext not in valid:
        raise ValidationError("Unsupported file extension.")


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,
                                   limit_choices_to={'is_submit': True, })

    def __str__(self):
        return self.restaurant.name


class Item(models.Model):
    Item_category = [
        ('Starter', 'Starter'),
        ('Main course', 'Main course'),
        ('Beef', 'Beef'),
        ('Dessert', 'Dessert'),
        ('Drink', 'Drink'),
    ]

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=20,
                            help_text="Maximum length is 20", )
    picture = models.ImageField(upload_to=get_upload_path_picture, validators=[custom_image_validator, ])
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0,
                                help_text="Maximum digit is 99.99", )
    category = models.CharField(max_length=11, choices=Item_category, )
    description = models.TextField(max_length=450,
                                   help_text="Maximum length is 450", )

    def save(self, *args, **kwargs):
        self.full_clean()

        self.picture = compress_image(self.picture, 50)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
