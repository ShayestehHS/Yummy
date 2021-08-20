from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.messages import get_messages
from Users.models import User

login_url = reverse("login")
signUp_url = reverse('sign_up')
logOut_url = reverse('logout')


def post_ajax(url, data, client):
    res = client.post(url, data=data,
                      content_type='application/json',
                      HTTP_X_REQUESTED_WITH='XMLHttpRequest', )
    return res


def create_data(username, email, conf=False):
    data = {
        'username': username,
        'email': email,
        'first_name': 'FirstName',
        'last_name': 'LastName',
        'password': 'Password123',
    }
    if conf:
        data.update({'confirm_password': data['password']})

    return data


class SignUpTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.setUp_user_data = create_data('setUp', 'setup@setup.com')
        self.setUp_user = get_user_model().objects.create_user(**self.setUp_user_data)
        return super(SignUpTest, self).setUp()

    def tearDown(self):
        return super(SignUpTest, self).tearDown()

    def test_AJAX_response_with_valid_value(self):
        """ Test AJAX response with valid email is return True """
        res = post_ajax(signUp_url, {'email': "AJAX@test.com"}, self.client)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(str(res.content, encoding='utf8'), {'email': "True"})

    def test_AJAX_response_with_invalid_value(self):
        """ Test AJAX response with exists email in database is return False """
        email = self.setUp_user_data['email']
        res = post_ajax(signUp_url, {'email': email}, self.client)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(str(res.content, encoding='utf8'), {'email': "False"})

    def test_SignUp_user_is_successfully(self):
        """ Test signUp function with valid data is successfully """
        user_data = create_data('SignUpTest', 'signUp@valid.com', conf=True)

        res = self.client.post(signUp_url, data=user_data)
        filtered_user = User.objects.filter(email=user_data['email'])

        self.assertTrue(filtered_user.exists())
        self.assertEqual(filtered_user.count(), 1)
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)

    def test_SignUp_user_with_exists_email(self):
        """ Test signUp function with exists email is fail """
        user_data = create_data('testUsername', self.setUp_user_data['email'])

        with self.assertRaises(Exception) as raised:
            res = self.client.post(signUp_url, data=user_data)

            self.assertEqual(IntegrityError, type(raised.exception))
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertIsNotNone(res.context['SUForm'])
            self.assertIsNotNone(res.context['SUForm'].errors)
            self.assertTemplateUsed(res, 'registration/login.html')

    def test_ConfirmEmail_creationCode_is_successfully(self):
        """ Test confirmEmailCode and uniqueCode is creating successfully """
        user_data = create_data('TestCreation', 'creation@test.com', conf=True)
        res_redirect = self.client.post(signUp_url, data=user_data)
        user = get_user_model().objects.get(email__exact=user_data['email'])

        self.assertIsNotNone(user.confirmEmailCode)
        self.assertIsNotNone(user.uniqueCode)

    def test_ConfirmEmail_with_valid_code(self):
        user_data = create_data('ConfirmEmailUName', 'confirmValid@email.com', conf=True)

        res_redirect = self.client.post(signUp_url, data=user_data)
        created_user = get_user_model().objects.get(email=user_data['email'])
        res = self.client.post(res_redirect['location'],
                               data={'Email_Code': created_user.confirmEmailCode,
                                     'UserCode': created_user.uniqueCode, }, )

        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual(res['location'], reverse('home'))

    def test_ConfirmEmail_with_invalid_code(self):
        user_data = create_data('ConfirmEmailUName', 'confirm@invalid.com', conf=True)

        res_redirect = self.client.post(signUp_url, data=user_data)
        created_user = User.objects.get(email__exact=user_data['email'])
        res = self.client.post(res_redirect['location'], data={'Email_Code': created_user.confirmEmailCode + 1,
                                                               'UserCode': created_user.uniqueCode, }, )

        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual(res['location'], reverse('ConfirmEmail',
                                                  kwargs={'UserCode': created_user.uniqueCode}))


class LoginTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.setUp_user_data = create_data('loginUsername', 'login@test.com')
        self.setUp_user = get_user_model().objects.create_user(**self.setUp_user_data)
        return super(LoginTest, self).setUp()

    def tearDown(self):
        return super(LoginTest, self).tearDown()

    def test_login_with_valid_data(self):
        """ Test login function with valid data is successfully """
        next_page = reverse('home')
        res = self.client.post(login_url, data={'email': self.setUp_user_data['email'],
                                                'password': self.setUp_user_data['password'],
                                                'next': next_page, })

        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual(res['location'], next_page)

    def test_login_with_invalid_password(self):
        """ Test login function with invalid password is fail """
        res = self.client.post(login_url, data={'email': self.setUp_user_data['email'],
                                                'password': "WrongPassword", }, )

        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual(res['location'], reverse('register'))

    def test_login_with_invalid_email(self):
        """ Test login function with invalid email address is fail """
        res = self.client.post(login_url, data={'email': 'login@invalid.com',
                                                'password': self.setUp_user_data['password'], })

        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual(res['location'], reverse('register'))


class LogoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = create_data('logoutUsername', 'login@test.com')
        self.setUp_user = get_user_model().objects.create_user(**self.user_data)
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        return super(LogoutTest, self).setUp()

    def test_logout(self):
        """ Test logout function with authenticated user is working successfully """
        res = self.client.get(logOut_url)

        self.assertTrue(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual(res['location'], reverse('home'))

    def test_not_authenticated_logout(self):
        """ Test logout function with anonymous user is fail """
        self.setUp_user = self.client.logout()

        res = self.client.get(logOut_url)
        messages = [str(message) for message in list(get_messages(res.wsgi_request))]

        self.assertTrue(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual(res['location'], reverse('home'))
        self.assertIn("You can't logging out right now", messages)
