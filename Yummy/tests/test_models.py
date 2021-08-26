import io

from PIL import Image
from django.core.exceptions import ValidationError
from django.test import TestCase
from Yummy.models import Restaurant
from django.contrib.auth import get_user_model


def generate_photo_file(pic_format='.png'):
    file = io.BytesIO()
    image = Image.new('RGBA', (800, 1200), (255, 255, 255))
    image.save(file, 'png')
    file.name = 'test' + pic_format
    file.seek(0)
    return file


class PublicModelTest(TestCase):
    def setUp(self):
        user_data = {
            'username': 'modelUsernmae',
            'email': 'model@test.com',
            'first_name': 'test',
            'last_name': 'testian',
            'password': 'Password123',
            'isOwner': True,
        }
        self.user = get_user_model().objects.create_user(**user_data)

        super(PublicModelTest, self).setUp()

    def tearDown(self):
        super(PublicModelTest, self).tearDown()

    def test_creating_restaurant_model_is_successfully(self):
        """ Test creating Restaurant model with valid data is successfully """
        restaurant_data = {
            'owner': self.user,
            'name': 'test restaurant',
            'logo': generate_photo_file(),
            'phone_number': 1234567,
            'email': 'restaurant@test.com',
            'website_url': 'https://restaurantTest.com',
            'postal_code': 123,
            'description': 'Long description text about restaurant',
            'delivery_charge': 10,
        }
        Restaurant.objects.create(**restaurant_data)

        self.assertTrue(Restaurant.objects.filter(name=restaurant_data['name']).exists())

    def test_creating_restaurant_model_with_exists_name(self):
        """ Test creating new Restaurant with duplicated name is raising error """
        restaurant_name = 'test restaurant'
        user_data_second = {
            'username': 'second owner',
            'email': 'owner@test.com',
            'first_name': 'test',
            'last_name': 'testian',
            'password': 'Password123',
            'isOwner': True,
        }
        restaurant_data_first = {
            'name': restaurant_name,
            'logo': generate_photo_file(),
            'phone_number': 1234567,
            'email': 'restaurant@test.com',
            'website_url': 'https://restaurantTest.com',
            'postal_code': 123,
            'description': 'Long description text about restaurant',
            'delivery_charge': 10,
        }
        restaurant_data_second = {
            'name': restaurant_name,
            'logo': generate_photo_file(),
            'phone_number': 1234567,
            'email': 'restaurant@test.com',
            'website_url': 'https://restaurantTest.com',
            'postal_code': 123,
            'description': 'Long description text about restaurant',
            'delivery_charge': 10,
        }

        user_second = get_user_model().objects.create_user(**user_data_second)
        Restaurant.objects.create(owner=self.user, **restaurant_data_first)

        with self.assertRaisesRegex(ValidationError, 'Restaurant with this Name already exists.'):
            Restaurant.objects.create(owner=user_second, **restaurant_data_second)

        self.assertFalse(Restaurant.objects.filter(owner=user_second,
                                                   name=restaurant_data_second['name']).exists())
