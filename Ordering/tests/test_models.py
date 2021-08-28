import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

from Menu.models import Item, Menu
from Ordering.models import Order, OrderDetail, CartItem
from Yummy.models import Restaurant

ordering_tests_dir = os.path.dirname(__file__)


class OrderingModelTest(TestCase):
    def setUp(self):
        user_data = {
            'username': 'orderModel user',
            'email': 'order@user.com',
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
            'name': 'Order restaurant',
            'phone_number': 9396527181,
            'website_url': 'https://www.order-restaurant.com',
            'email': 'order@restaurant.com',
            'logo': SimpleUploadedFile(**test_png_data),
            'description': 'long description',
            'delivery_charge': 12,
            'is_delivery': True,
            'is_take_away': False,
            'postal_code': 1234,
            'long': 12.123456,
            'lat': 12.123456,
        }
        item_data = {
            'picture': SimpleUploadedFile(**test_png_data),
            'price': 12,
            'category': 'Drink',
            'description': 'Short description',
        }

        self.user = get_user_model().objects.create_user(**user_data)
        self.order = Order.objects.create(user=self.user)

        self.client = Client()
        self.restaurant = Restaurant.objects.create(owner=self.user, **restaurant_data)
        self.menu = Menu.objects.create(restaurant=self.restaurant)
        self.item_1 = Item.objects.create(menu=self.menu, name='item_1', **item_data)
        self.item_2 = Item.objects.create(menu=self.menu, name='item_2', **item_data)
        self.item_3 = Item.objects.create(menu=self.menu, name='item_3', **item_data)

        super(OrderingModelTest, self).setUp()

    def tearDown(self):
        super(OrderingModelTest, self).tearDown()

    def test_creating_order_model_without_restaurant_is_successfully(self):
        """ Test creating Order object without restaurant is working correctly """
        user_data = {
            'username': 'user without order',
            'email': 'without@order.com',
            'first_name': 'test',
            'last_name': 'testian',
            'password': 'Password123',
        }
        user = get_user_model().objects.create_user(**user_data)

        Order.objects.create(user=user)

        self.assertTrue(Order.objects.filter(user=user).exists())
        self.assertFalse(Order.objects.get(user=user).is_paid)

    def test_adding_item_to_order_model_is_add_one_to_quantity(self):
        """ Test Add function is
            add 1 to the quantity of CartItem
            and
            increase price of Item to ( total_price of CartItem ) and ( payout of Order ) """
        cart_item_1 = CartItem.objects.create(order=self.order, item=self.item_1)
        cart_item_1.Add()  # quantity = 1 ** payout = self.item_1.price * 1
        cart_item_1.Add()  # quantity = 2 ** payout = self.item_1.price * 2

        self.assertEqual(CartItem.objects.get(order=self.order, item=self.item_1).quantity, 2)
        self.assertEqual(cart_item_1.total_price, self.item_1.price * 2)
        self.assertEqual(self.order.payout, self.item_1.price * 2)

    def test_removing_item_from_order_model_is_successfully(self):
        """ Test Remove function is
            minus 1 from the quantity of CartItem
            and
            decrease price of Item from ( total_price of CartItem ) and ( payout of Order ) """
        cart_item_1 = CartItem.objects.create(order=self.order, item=self.item_1)
        cart_item_1.Add()  # quantity = 1 ** payout = self.item_1.price * 1
        cart_item_1.Add()  # quantity = 2 ** payout = self.item_1.price * 2
        cart_item_1.Add()  # quantity = 3 ** payout = self.item_1.price * 3

        cart_item_1.Remove()  # quantity = (3-1) ** payout = self.item_1.price * (3-1)

        self.assertEqual(CartItem.objects.get(order=self.order, item=self.item_1).quantity, 2)
        self.assertEqual(cart_item_1.total_price, self.item_1.price * 2)
        self.assertEqual(self.order.payout, self.item_1.price * 2)

    def test_set_wrong_choice_for_deliveryDay_raise_error(self):
        """ Test on creation of OrderDetail,
            if user send invalid choice for delivery_day, model raise ValidationError """
        order_detail_data = {
            'order': self.order,
            'telephone': 123456789,
            'full_address': 'This is a long text',
            'postal_code': 12345,
            'delivery_day': 'invalid choice',
            'delivery_time': '12.30am',
            'delivery_method': 'Delivery',
            'description': 'Long description'
        }
        with self.assertRaisesRegex(ValidationError, "Value 'invalid choice' is not a valid choice."):
            OrderDetail.objects.create(**order_detail_data)

    def test_set_wrong_choice_for_deliveryMethod_raise_error(self):
        """ Test on creation of OrderDetail,
           if user send invalid choice for deliveryMethod, model raise ValidationError """
        order_detail_data = {
            'order': self.order,
            'telephone': 123456789,
            'full_address': 'This is a long text',
            'postal_code': 12345,
            'delivery_day': 'Today',
            'delivery_time': '12.30am',
            'delivery_method': 'Wrong method',
            'description': 'Long description'
        }
        with self.assertRaisesRegex(ValidationError, "Value 'Wrong method' is not a valid choice."):
            OrderDetail.objects.create(**order_detail_data)
