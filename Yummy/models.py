import os

from ckeditor.fields import RichTextField
from django.db import models
from mapbox import Geocoder
from taggit.managers import TaggableManager
from Yummy_site.settings import TESTING

from Yummy_site import settings
from Yummy_site.settings import MAPBOX_KEY
from utility import Compress


def get_upload_path_for_logo(instance, filename):
    return os.path.join('Restaurant', f'{instance.name}', filename)


def get_upload_path_for_image(instance, filename):
    return os.path.join('Restaurant', f'{instance.restaurant.name}', 'image',
                        filename)


class Restaurant(models.Model):
    owner = models.OneToOneField(to=settings.AUTH_USER_MODEL,
                                 related_name='owner',
                                 null=True, blank=True,
                                 on_delete=models.CASCADE,
                                 limit_choices_to={'isOwner': True})
    name = models.CharField(max_length=40, unique=True,
                            help_text="Maximum length is 40", )
    logo = models.ImageField(upload_to=get_upload_path_for_logo)
    tags = TaggableManager()
    phone_number = models.IntegerField()
    email = models.EmailField()
    website_url = models.URLField(null=True)
    postal_code = models.IntegerField()
    rating = models.DecimalField(decimal_places=3, max_digits=4,
                                 blank=True, null=True, )
    description = RichTextField()
    delivery_charge = models.IntegerField(default=0,
                                          help_text="Just whole numbers are acceptable.")
    is_delivery = models.BooleanField(default=False)
    is_take_away = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_submit = models.BooleanField(default=False, )
    # Address
    address = models.CharField(max_length=60, default='address')
    long = models.DecimalField(max_digits=8, decimal_places=6,
                               default=51.337888)
    lat = models.DecimalField(max_digits=8, decimal_places=6,
                              default=35.699784)
    city = models.CharField(max_length=15, null=False, default='city')

    def save(self, *args, **kwargs):
        self.logo = Compress.compress_image(self.logo, 30)
        self.full_clean()
        if not TESTING and not self.pk:
            # on 'Create' or TESTING is False
            geocoder = Geocoder(access_token=MAPBOX_KEY)
            response = geocoder.reverse(lat=self.lat, lon=self.long)
            features = sorted(response.geojson()['features'],
                              key=lambda x: x['place_name'])
            for f in features:
                place_type = f.get('place_type')
                if place_type == ['place'] or place_type == ['region']:
                    self.address = place_type
                    break

        super(Restaurant, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class OpeningTime(models.Model):
    WEEKDAYS = [
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,
                                   related_name='Opening_time')
    weekday = models.CharField(choices=WEEKDAYS, max_length=9)
    from_hour = models.TimeField(null=True, blank=True)
    to_hour = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ('weekday', 'from_hour')

    def __unicode__(self):
        return f'restaurant name:{self.restaurant.name} :: {self.get_weekday_display()}: {self.from_hour} - {self.to_hour} '


class RestaurantImage(models.Model):
    """ Image of slider in detail_restaurant.html"""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,
                                   default=None)
    image = models.FileField(upload_to=get_upload_path_for_image)

    def delete(self, using=None, keep_parents=True):
        # Delete Photo when => user delete image
        img_path = self.image.path
        if os.path.isfile(img_path):
            os.remove(img_path)
        # Call the "real" save() method.
        super(RestaurantImage, self).delete()

    def save(self, *args, **kwargs):
        self.image = Compress.compress_image(self.image)
        if os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super(RestaurantImage, self).save(*args, **kwargs)

    def __str__(self):
        return self.image.name


class RestaurantReview(models.Model):
    decimal_help_text = "Maximum number is 9999.999"
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    food_quality = models.DecimalField(decimal_places=3, max_digits=4,
                                       help_text=decimal_help_text)
    price = models.DecimalField(decimal_places=3, max_digits=4,
                                help_text=decimal_help_text)
    punctuality = models.DecimalField(decimal_places=3, max_digits=4,
                                      help_text=decimal_help_text)
    courtesy = models.DecimalField(decimal_places=3, max_digits=4,
                                   help_text=decimal_help_text)
    description = models.TextField(max_length=200,
                                   help_text="Maximum length is 200")

    created_date = models.DateField(auto_now_add=True)

    def delete(self, using=None, keep_parents=True):
        count = self.restaurant.restaurantreview_set.count()
        # Calculating average of rates
        last_average = self.restaurant.rating
        sum_all_field = (
                self.food_quality + self.price + self.punctuality + self.courtesy)
        average_rating = ((last_average * count * 4) - sum_all_field) / (
                4 * (count - 1))

        restaurant = Restaurant.objects.filter(pk=self.restaurant.pk).first()
        restaurant.update(rating=average_rating)
        super(RestaurantReview, self).delete()

    def save(self, *args, **kwargs):
        count = self.restaurant.restaurantreview_set.count()
        # Calculating average of rates
        last_average = self.restaurant.rating if self.restaurant.rating is not None else 0
        sum_all_field = (
                self.food_quality + self.price + self.punctuality + self.courtesy)
        average_rating = ((last_average * count * 4) + sum_all_field) / (
                4 * (count + 1))
        restaurant = Restaurant.objects.get(pk=self.restaurant.pk)
        restaurant.rating = average_rating
        restaurant.save(update_fields=['rating'])
        super(RestaurantReview, self).save(*args,
                                           **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return f'{self.restaurant.name} : {self.user.username}'
