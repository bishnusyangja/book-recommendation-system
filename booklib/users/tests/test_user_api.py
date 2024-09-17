from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User
from model_bakery import baker


class RegistrationAPITestCase(TestCase):
    client = APIClient()
    url = '/register/'

    def test_user_register_with_empty_data(self):
        data = {}
        resp = self.client.post(self.url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_user_registration_with_valid_data(self):
        passwd = 'Newis#$new234'
        data  = {'first_name': 'Ramesh Raj', 'last_name': 'Bhattarai', 'email': 'pqrs@gmail.com',
                 'password': passwd, 'confirm_password': passwd}
        resp = self.client.post(self.url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 201)

    def test_user_registration_with_passwd_doesnot_match(self):
        passwd = 'Newis#$new234'
        data  = {'first_name': 'Ramesh Raj', 'last_name': 'Bhattarai', 'email': 'pqrs@gmail.com',
                 'password': passwd, 'confirm_password': 'jptramsiyaram'}
        resp = self.client.post(self.url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('password', resp.json().keys())

    def test_duplicate_email_registration(self):
        passwd = 'Newis#$new234'
        email = 'abcxyz@gmail.com'
        baker.make(User, email=email)
        data = {'first_name': 'Santosh', 'last_name': 'Sharma', 'email': email,
                'password': passwd, 'confirm_password': passwd}
        resp = self.client.post(self.url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('email', resp.json().keys())
