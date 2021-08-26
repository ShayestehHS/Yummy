from django.contrib.auth import get_user_model
from django.test import TestCase

from Users.models import Driver


class PublicUserModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a user with email is successful"""
        email = "test@test.com"
        user_data = {
            'email': email,
            'username': 'testUsername',
            'first_name': "test",
            'last_name': "testy",
            'password': "Password123",
        }

        user = get_user_model().objects.create_user(**user_data)

        self.assertEqual(user.email, email)

    def test_create_superuser_with_email_successful(self):
        """Test creating a superuser with email is successful"""
        email = "Hossein@shayesteh.com"
        superuser = get_user_model().objects.create_superuser(
            email=email,
            username='testUsername',
            first_name="test",
            last_name="testy",
            password="Password123",
        )
        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.is_superuser)

    def test_hashing_password(self):
        """Test after creating a user, input password is hashed"""
        password = "Password123"
        user_data = {
            'email': "test@test.com",
            'username': 'testUsername',
            'first_name': "test",
            'last_name': "testy",
            'password': password,
        }

        user = get_user_model().objects.create_user(**user_data)

        self.assertNotEqual(user.password, password)


class PrivateUserModelTest(TestCase):
    def setUp(self):
        user_data = {
            'email': "private@test.com",
            'username': 'privateModel',
            'first_name': "test",
            'last_name': "testian",
            'password': "Password123",
        }
        self.user = get_user_model().objects.create_user(**user_data)

        self.client.force_login(self.user)
        return super(PrivateUserModelTest, self).setUp()

    def tearDown(self):
        return super(PrivateUserModelTest, self).tearDown()

    def test_create_driver(self):
        """Test creating driver is successfully"""
        driver = Driver.objects.create(
            user=self.user,
            phone_number=123456789,
            motorbike=True,
            student=True,
            driver_lic=True,
            mobile=True,
        )

        driver.refresh_from_db()
        self.assertEqual(driver, Driver.objects.get(user=self.user))
        self.assertEqual(driver.user, self.user)
