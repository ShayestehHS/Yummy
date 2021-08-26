import os
import time

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from Users.models import Driver
from Yummy.forms import DriverForm, Review_Form, SubmitRestaurantForm
from Yummy.models import OpeningTime, Restaurant, RestaurantReview
from utility.opening_utility import get_opening_times

yummy_test_dir = os.path.dirname(__file__)


class PublicYummyViewsTest(TestCase):
    def setUp(self):
        pic = SimpleUploadedFile(name='test_image.jpg',
                                 content=open(os.path.join(yummy_test_dir, 'test.png'), 'rb').read(),
                                 content_type='image/jpeg')
        self.owner_data = {
            "username": 'public owner',
            "email": 'public@owner.com',
            "first_name": 'test',
            "last_name": 'testian',
            "isOwner": True,
        }
        self.restaurant_data = {
            'name': 'public restaurant',
            'phone_number': 9396527181,
            'website_url': 'https://www.public-restaurant.com',
            'email': 'public@restaurant.com',
            'description': 'long description',
            'delivery_charge': 12,
            'is_delivery': True,
            'is_take_away': False,
            'postal_code': 1234,
            'long': 12.123456,
            'lat': 12.123456,
        }

        self.owner = get_user_model().objects.create(**self.owner_data)
        self.restaurant = Restaurant.objects.create(owner=self.owner, **self.restaurant_data, logo=pic)
        self.client = Client()

        self.restaurant.tags.add('test_tag', 'taggit')
        super(PublicYummyViewsTest, self).setUp()

    def tearDown(self):
        super(PublicYummyViewsTest, self).tearDown()

    def test_listing_restaurants_is_successful(self):
        """ Test listing restaurants in list page is successfully """
        res = self.client.get(reverse('list', kwargs={'page': 1}))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'restaurant/list_page.html')
        self.assertEqual(res.context['allRestaurant_Count'], Restaurant.objects.all().count())

    def test_listing_restaurants_in_grid_list_is_successful(self):
        """ Test listing restaurants in grid page is successfully """
        res = self.client.get(reverse('grid_list', kwargs={'page': 1}))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'restaurant/grid_list.html')
        self.assertEqual(res.context['allRestaurant_Count'], Restaurant.objects.all().count())

    def test_get_detail_of_restaurant_by_id(self):
        """ Test getting detail, pictures and comments of restaurant by id """
        res = self.client.get(reverse('detail_restaurant', kwargs={'Re_id': self.restaurant.id}))
        context = res.context
        opening_time = OpeningTime.objects.filter(
            restaurant=self.restaurant).values_list('weekday', 'from_hour', 'to_hour')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'restaurant/detail_restaurant.html')
        self.assertEqual(context['restaurant'], self.restaurant)
        self.assertEqual(context['image'].count(), self.restaurant.restaurantimage_set.count())
        self.assertEqual(context['review'].count(), self.restaurant.restaurantreview_set.count())
        self.assertEqual(context['today_weekday'], get_opening_times(opening_time))
        self.assertEqual(context['form'], Review_Form)

    def test_search_between_name_of_restaurants(self):
        """ Test search functionality by GETing key from request """
        res = self.client.get(reverse('search', kwargs={'page': 1}),
                              data={'key': self.restaurant.name})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'restaurant/list_page.html')
        self.assertEqual(res.context['searched_key'], self.restaurant.name)
        self.assertIn(self.restaurant, list(res.context['allRestaurant']))

    def test_contact_to_us_rendering_correctly(self):
        """ Test contact_to_us with GET method is rendering the page """
        res = self.client.get(reverse('contacts'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'main_pages/contacts.html')

    def test_contact_to_us_posting_email_to_super_user(self):
        """ Test sending email to super user with AJAX is working correctly """
        self.owner.is_superuser = True
        self.owner.save(update_fields=['is_superuser'])
        email_data = {
            'name': 'test',
            'family': 'testian',
            'email': 'contacts@ToUs.com',
            'text': 'This is a long text from test testian',
        }
        res = self.client.post(reverse('contacts'), data=email_data,
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest', )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertJSONEqual(str(res.content, encoding='utf8'),
                             {'success': "We received your emailThanks for your email", })


class PrivateYummyViewsTest(TestCase):
    def setUp(self):
        pic = SimpleUploadedFile(name='test_image.jpg',
                                 content=open(os.path.join(yummy_test_dir, 'test.png'), 'rb').read(),
                                 content_type='image/jpeg')
        user_data = {
            'username': 'private yummy',
            'email': 'private@test.com',
            'first_name': 'test',
            'last_name': 'testian',
            'password': 'Password123',
        }
        owner_data = {
            "username": 'private owner',
            "email": 'private@owner.com',
            "first_name": 'test',
            "last_name": 'testian',
            "isOwner": True,
        }
        restaurant_data = {
            'name': 'private restaurant',
            'phone_number': 9396527181,
            'website_url': 'https://www.private-restaurant.com',
            'email': 'private@restaurant.com',
            'description': 'long description',
            'tags': 'test_tag,test',
            'delivery_charge': 12,
            'is_delivery': True,
            'is_take_away': False,
            'postal_code': 1234,
            'long': 12.123456,
            'lat': 12.123456,
        }

        self.client = Client()
        self.user = get_user_model().objects.create(**user_data)
        self.owner = get_user_model().objects.create(**owner_data)
        self.restaurant = Restaurant.objects.create(owner=self.owner, **restaurant_data, logo=pic)

        self.client.force_login(self.user)
        super(PrivateYummyViewsTest, self).setUp()

    def tearDown(self):
        super(PrivateYummyViewsTest, self).tearDown()

    def test_submit_driver_with_get_method(self):
        """ Test submit driver with Get method is sending DriverForm to user """
        res = self.client.get(reverse('submit_driver'))

        self.assertEqual(res.context['form'], DriverForm)

    def test_submit_driver_with_post_method(self):
        """ Test submit DriverForm by user is working correctly """
        DriverForm_data = {
            'phone_number': 9396527181,
            'motorbike': 'Yes',
            'student': 'Yes',
            'driver_lic': 'Yes',
            'mobile': 'Yes',
        }
        res = self.client.post(reverse('submit_driver'), data=DriverForm_data)

        created_driver = Driver.objects.filter(user=self.user)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual(res['location'], reverse('home'))
        self.assertTrue(created_driver.exists())
        self.assertEqual(created_driver.count(), 1)
        self.assertTrue(DriverForm_data['mobile'], created_driver.first().mobile)
        self.assertTrue(self.user.isDriver)

    def test_submit_driver_send_error_message_to_driver(self):
        """ Test sending error message to user that submitted as driver before """
        self.user.isDriver = True
        self.user.save(update_fields=['isDriver'])

        res = self.client.get(reverse('submit_driver'))

        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual(res['location'], reverse('home'))

    def test_submit_restaurant_with_get_method(self):
        """ Test submit restaurant with Get method is sending SubmitRestaurantForm to user """
        res = self.client.get(reverse('submit_restaurant'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'submission/submit_restaurant.html')
        self.assertEqual(res.context['form'], SubmitRestaurantForm)

    def test_submit_restaurant_with_post_method(self):
        """ Test submit SubmitRestaurantForm by user is working correctly """
        SubmitRestaurantForm_data = {
            'name': 'test restaurant',
            'phone_number': 9396527181,
            'website_url': 'https://www.test-restaurant.com',
            'email': 'test@restaurant.com',
            'description': 'long description',
            'tags': 'test_tag,test',
            'delivery_charge': 12,
            'is_delivery': True,
            'is_take_away': False,
            'postal_code': 1234,
            'long': 12.123456,
            'lat': 12.123456,
        }

        with open(os.path.join(yummy_test_dir, 'test.png'), 'rb') as pic:
            SubmitRestaurantForm_data['logo'] = pic
            res = self.client.post(reverse('submit_restaurant'), data=SubmitRestaurantForm_data)
        created_restaurant = Restaurant.objects.filter(owner=self.user)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual(res['location'], reverse('home'))
        self.assertTrue(created_restaurant.exists())
        self.assertEqual(created_restaurant.count(), 1)
        self.assertTrue(SubmitRestaurantForm_data['name'], created_restaurant.first().name)
        self.assertTrue(self.user.isOwner)

    def test_submit_restaurant_send_error_message_to_owner(self):
        """ Test sending error message to user that submitted as owner before """
        self.user.isOwner = True
        self.user.save(update_fields=['isOwner'])

        res = self.client.get(reverse('submit_restaurant'))

        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual(res['location'], reverse('home'))
        self.assertIsNone(res.context)

    def test_saving_review_with_ajax_and_post_method(self):
        """ Test saving_review function is working correctly """
        Review_data = {
            'food_quality': 1, 'price': 2,
            'punctuality': 3, 'courtesy': 4,
            'description': 'long description',
        }
        res = self.client.post(reverse('save_review', kwargs={'Re_id': self.restaurant.id}),
                               data=Review_data,
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest', )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(b'success', res.content)
        self.assertIn(b'review', res.content)
        self.assertTrue(RestaurantReview.objects.filter(user=self.user).exists())
