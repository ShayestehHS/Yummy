import os

from django.db import models

from Yummy.models import Restaurant
from utility.Compress import compress_image


def get_upload_path_picture(instance, filename):
    return os.path.join('Restaurant', f'{instance.menu.restaurant.name}',
                        'Menu', f'{instance.category}', filename)


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

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
    name = models.CharField(max_length=20, help_text="Maximum length is 20")
    picture = models.ImageField(upload_to=get_upload_path_picture)
    price = models.DecimalField(max_digits=3, decimal_places=2,
                                help_text="Maximum digit is 999.99", default=0)
    category = models.CharField(max_length=11, choices=Item_category,
                                help_text="Maximum length is 11")
    description = models.TextField()

    def save(self, *args, **kwargs):
        self.picture = compress_image(self.picture, 50)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
