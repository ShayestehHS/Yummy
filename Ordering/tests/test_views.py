from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
import os

from django.urls import reverse
from rest_framework import status

from Menu.models import Item, Menu
from Ordering.models import CartItem, Order, OrderDetail
from Yummy.models import Restaurant

ordering_tests_dir = os.path.dirname(__file__)


class PrivateOrderingViewsTest(TestCase):
    def setUp(self):
        user_data = {
            'username': 'ordering username',
            'email': 'ordering@test.con',
            'first_name': 'test',
            'last_name': 'testian',
            'password': 'Password123'
        }
        owner_data = {
            'username': 'owner ordering',
            'email': 'owner@ordering.con',
            'first_name': 'test',
            'last_name': 'testian',
            'password': 'Password123',
            'isOwner': True,
        }
        test_png_data = {
            'name': 'test.jpg',
            'content': open(os.path.join(ordering_tests_dir, 'test.png'), 'rb').read(),
            'content_type': 'image/jpeg'
        }
        restaurant_data = {
            'name': 'private ordering',
            'phone_number': 9396527181,
            'website_url': 'https://www.private-ordering.com',
            'email': 'private@ordering.com',
            'logo': SimpleUploadedFile(**test_png_data),
            'description': 'long description',
            'delivery_charge': 12,
            'is_delivery': True,
            'is_take_away': False,
            'postal_code': 1234,
            'long': 12.123456,
            'lat': 12.123456,
        }
        item_1_data = {
            'name': 'item_1 drink',
            'description': 'long description',
            'category': 'Drink',
            'price': 12,
            'picture': SimpleUploadedFile(**test_png_data),
        }

        self.client = Client()
        self.user = get_user_model().objects.create_user(**user_data)
        self.owner = get_user_model().objects.create_user(**owner_data)
        self.restaurant = Restaurant.objects.create(owner=self.owner, **restaurant_data)
        self.menu = Menu.objects.create(restaurant=self.restaurant)
        self.item_1 = Item.objects.create(menu=self.menu, **item_1_data)
        self.order = Order.objects.create(user=self.user, restaurant=self.restaurant)
        self.cart_item_1 = CartItem.objects.create(order=self.order, item=self.item_1)

        self.client.force_login(self.user)
        super(PrivateOrderingViewsTest, self).setUp()

    def tearDown(self):
        super(PrivateOrderingViewsTest, self).tearDown()

    def test_step_1_redirect_user_if_Order_is_empty(self):
        """ Test GET method of step_1 is redirect user to home if Order is empty """
        res = self.client.get(reverse('step_1'))

        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual(res['location'], reverse('home'))

    def test_step_1_with_get_method_working_correctly(self):
        """ Test GET method of step_1 is rendering the page correctly """
        self.cart_item_1.Add()

        res = self.client.get(reverse('step_1'))
        order = Order.objects.get(user=self.user, is_paid=False)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'ordering/step_1.html')
        self.assertEqual(res.context['order_list'], order)

    def test_step_1_with_post_method_working_correctly(self):
        """ Test POST method of step_1 is save order_detail correctly """
        step1_form_data = {
            'telephone': 123456,
            'full_address': 'This is a short text',
            'postal_code': 123456,
            'delivery_day': 'Today',
            'delivery_time': '17:30',
            'delivery_method': 'Delivery',
        }
        self.cart_item_1.Add()

        res = self.client.post(reverse('step_1'), data=step1_form_data)
        order_detail = OrderDetail.objects.filter(order=self.order, order__user=self.user)

        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertTrue(order_detail.exists())
        self.assertEqual(order_detail.first().telephone, step1_form_data['telephone'])
        self.assertEqual(order_detail.first().full_address, step1_form_data['full_address'])

    def test_step_2_prevent_from_loading(self):
        """ Test if OrderDetail of user is not exits: User is redirecting to step_1 """
        res = self.client.get(reverse('step_2'))
        res_messages = [m.message for m in messages.get_messages(res.wsgi_request)]

        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual(res['location'], reverse('step_1'))
        self.assertEqual(len(res_messages), 1)
        self.assertIn('You have to complete step_one first', res_messages)

    def test_step_3_working_correctly(self):
        """ Test step_3 function is working correctly """
        order_detail_data = {
            'order': self.order,
            'telephone': 123456,
            'full_address': 'This is a short text',
            'postal_code': 123456,
            'delivery_day': 'Today',
            'delivery_time': '17:30',
            'delivery_method': 'Delivery',
        }
        OrderDetail.objects.create(**order_detail_data)

        res = self.client.get(reverse('step_3'))
        res_messages = [m.message for m in messages.get_messages(res.wsgi_request)]
        old_order = Order.objects.filter(user=self.user, is_paid=False)
        new_order = Order.objects.filter(user=self.user, is_paid=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'ordering/step_3.html')
        self.assertEqual(len(res_messages), 1)
        self.assertIn("Your order is on the way", res_messages)
        self.assertTrue(old_order.exists())
        self.assertTrue(new_order.exists())

    def test_update_cart_with_plus_mode(self):
        """ Test adding item to Order with AJAX """
        self.cart_item_1.Add()  # Quantity = 1
        self.cart_item_1.Add()  # Quantity = 2
        item_data = {
            'item_id': self.item_1.id,
            'item_mode': 'plus',
        }  # Quantity = 3

        res = self.client.post(reverse('updateCarts'), data=item_data,
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.cart_item_1.refresh_from_db()
        expected_json = {'quantity': 3, 'total_price': str(self.cart_item_1.total_price)}

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(str(res.content, encoding='utf8'), expected_json)

    def test_update_cart_with_minus_mode(self):
        """ Test removeing item to Order with AJAX """
        self.cart_item_1.Add()  # Quantity = 1
        self.cart_item_1.Add()  # Quantity = 2
        item_data = {
            'item_id': self.item_1.id,
            'item_mode': 'minus',
        }  # Quantity = 1

        res = self.client.post(reverse('updateCarts'), data=item_data,
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.cart_item_1.refresh_from_db()
        expected_json = {'quantity': 1, 'total_price': str(self.cart_item_1.total_price)}

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(str(res.content, encoding='utf8'), expected_json)
