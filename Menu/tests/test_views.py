import io
import json
import os

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from Menu.models import Menu, Item
from Ordering.models import Order
from Yummy.models import Restaurant


def post_ajax(url, dictionary, client):
    dictionary = json.dumps(dictionary)
    res = client.post(
        url, data=dictionary,
        content_type='application/json',
        HTTP_X_REQUESTED_WITH='XMLHttpRequest', )

    return res


def generate_photo_file(pic_format='.png'):
    file = io.BytesIO()
    image = Image.new('RGBA', (800, 1200), (255, 255, 255))
    image.save(file, 'png')
    file.name = 'test' + pic_format
    file.seek(0)
    return file


class PublicMenuViewTest(TestCase):
    def setUp(self):
        user_data = {
            "username": 'public Username',
            "email": 'public@test.com',
            "first_name": 'test',
            "last_name": 'testian',
            "isOwner": True,
        }
        restaurant_data = {
            "name": 'test restaurant',
            "logo": generate_photo_file(),
            "phone_number": 1234455,
            "email": 'restaurant@test.com',
            "website_url": 'https://www.test.com',
            "postal_code": 2323,
            "description": 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            "delivery_charge": 12,
        }

        self.client = Client()
        self.user = get_user_model().objects.create(**user_data)
        self.restaurant = Restaurant.objects.create(owner=self.user, **restaurant_data)
        self.menu = Menu.objects.create(restaurant=self.restaurant)

        super(PublicMenuViewTest, self).setUp()

    def tearDown(self):
        super(PublicMenuViewTest, self).tearDown()

    def test_filter_restaurants_with_valid_data_working(self):
        """ Test filtering in left_bar of list pages ( with valid data ) is working """
        self.restaurant.tags.add('test_tag')

        data = {
            'type': ['test_tag'],
            'rating': 1,
            'isDelivery': 'true',
            'isTakeAway': 'false',
            'popularity': 'false',
            'senderPath': 'http://test.com/list_page/1/',
        }
        res = post_ajax(reverse('filterAJAX', kwargs={'page': 1}), data, self.client)

        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateMenuViewsTest(TestCase):
    def setUp(self):
        user_data = {
            "username": 'private Username',
            "email": 'private@test.com',
            "first_name": 'test',
            "last_name": 'testian',
            "isOwner": True,
        }
        restaurant_data = {
            "name": 'test restaurant',
            "logo": generate_photo_file(),
            "phone_number": 1234455,
            "email": 'restaurant@test.com',
            "website_url": 'https://www.test.com',
            "postal_code": 2323,
            "description": 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            "delivery_charge": 12,
        }
        item_data = {
            'name': 'test',
            'picture': generate_photo_file(),
            'price': 12,
            'category': 'Drink',
            'description': 'Long text for description',
        }

        self.client = Client()
        self.user = get_user_model().objects.create(**user_data)
        self.restaurant = Restaurant.objects.create(owner=self.user, **restaurant_data)
        self.menu = Menu.objects.create(restaurant=self.restaurant)
        self.item = Item.objects.create(menu=self.menu, **item_data)

        self.client.force_login(self.user)
        super(PrivateMenuViewsTest, self).setUp()

    def tearDown(self):
        super(PrivateMenuViewsTest, self).tearDown()

    def test_getting_menu_by_restaurant_id(self):
        """ Test getting Menu objects of restaurant by restaurant id """
        Order.objects.create(user=self.user, restaurant=self.restaurant)
        res = self.client.get(reverse('menu', kwargs={'id': self.restaurant.id}))
        contexts = res.context

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(contexts['restaurant'], self.restaurant)
        self.assertTemplateUsed(res, 'restaurant/menu.html')

    def test_admin_section_loading_page_is_successful(self):
        """ Test getting admin section of restaurant is sending successfully """
        res = self.client.get(reverse('admin_section'))
        context = res.context

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'main_pages/admin_section.html')
        self.assertIsNotNone(context['restaurant'])
        self.assertIsNotNone(context['items'])
        self.assertIsNotNone(context['form'])

    def test_admin_section_delete_item(self):
        """ Test deleting item in admin section with AJAX is working correctly """
        data = {'item_ID': self.item.id}
        res = post_ajax(reverse('deleteItem_form'), data, self.client)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(str(res.content, encoding='utf8'), {'result': 'success'})
        self.assertFalse(Item.objects.filter(id=self.item.id).exists())

    def test_admin_section_add_item_functionality(self):
        """ Test adding item in admin section with AJAX is working correctly """
        menu_tests_dir = os.path.dirname(__file__)
        form_data = {
            'name': "Add item",
            'price': 14,
            'category': "Drink",
            'description': "long description text",
        }

        with open(os.path.join(menu_tests_dir, 'test.png'), 'rb') as pic:
            form_data['picture'] = pic
            res = self.client.post(reverse('addItem_form'), data=form_data,
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        filtered_item = Item.objects.filter(name=form_data['name'],
                                            category=form_data['category'])

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'restaurant/menu_items.html')
        self.assertIsNotNone(res.context['items'])
        self.assertEqual(1,filtered_item.count())
        self.assertEqual(self.menu,filtered_item.first().menu)
        self.assertTrue(filtered_item.exists())

    def test_admin_section_update_item_functionality(self):
        """ Test updating item in admin section with AJAX is working """
        data = {
            'id': self.item.id,
            'name': 'changedName',
            'category': 'Dessert',
            'price': 14,
            'description': 'Short description text',
        }
        res = post_ajax(reverse('updateItem_form'), data, self.client)
        updated_item = Item.objects.get(id=self.item.id)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(str(res.content, encoding='utf8'), {})
        self.assertEqual(updated_item.name, data['name'])
        self.assertEqual(updated_item.category, data['category'])
        self.assertEqual(updated_item.price, data['price'])
        self.assertEqual(updated_item.description, data['description'])
