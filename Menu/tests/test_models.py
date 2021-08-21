import io
from decimal import Decimal

from PIL import Image
from django.core.exceptions import ValidationError
from django.test import TestCase
from Menu.models import Menu, Item
from Yummy.models import Restaurant
from django.contrib.auth import get_user_model


def generate_photo_file(pic_format='.png'):
    file = io.BytesIO()
    image = Image.new('RGBA', (800, 1200), (255, 255, 255))
    image.save(file, 'png')
    file.name = 'test' + pic_format
    file.seek(0)
    return file


class ItemModelTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(
            username='itemModelUsername',
            email='ItemModel@test.com',
            first_name='test',
            last_name='testian',
            isOwner=True, )
        restaurant = Restaurant.objects.create(
            owner=user,
            name='test restaurant',
            logo=generate_photo_file(),
            phone_number=1234455,
            email='restaurant@test.com',
            website_url='https://www.test.com',
            postal_code=2323,
            description='Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            delivery_charge=12, )

        self.menu = Menu.objects.create(restaurant=restaurant)

        super(ItemModelTest, self).setUp()

    def tearDown(self):
        super(ItemModelTest, self).tearDown()

    def test_creation_item_with_valid_data(self):
        """ Test creation Item object with valid data is successful """
        Item.objects.create(
            menu=self.menu,
            name='test',
            category='Drink',
            price=12.0,
            picture=generate_photo_file(),
            description="Long description text",
        )

        self.assertTrue(Item.objects.filter(menu=self.menu, name='test').exists())

    def test_creation_item_with_invalid_category(self):
        """ Test creation Item object with invalid category is fail """
        with self.assertRaisesRegex(ValidationError, "Value 'invalid' is not a valid choice."):
            Item.objects.create(
                menu=self.menu,
                name='test item',
                description='long description',
                category='invalid',
                price=12,
                picture=generate_photo_file(),
            )

        self.assertFalse(Item.objects.filter(menu=self.menu, name='test item').exists())

    def test_creation_item_with_invalid_picture_format(self):
        """ Test crating Item with invalid picture form is fail """
        item_data = {
            'menu': self.menu,
            'name': 'test invalid format',
            'description': 'long description',
            'category': 'invalid',
            'price': 12,
            'picture': generate_photo_file(".rpg"),
        }
        with self.assertRaisesRegex(ValidationError, "Unsupported file extension."):
            Item.objects.create(**item_data)

        self.assertFalse(Item.objects.filter(menu=self.menu, name='test invalid format').exists())
