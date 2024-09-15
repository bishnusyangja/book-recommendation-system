from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APIClient

from users.models import User

EMAIL = 'abc@gmail.com'
PASSWD = 'random_string@$&123'

class APITokenTestCase(TestCase):
    client = APIClient()
    url = '/api/token/'
    email = EMAIL
    password = PASSWD

    def test_api_token(self):
        user = baker.make(User, email=self.email)
        user.set_password(self.password)
        user.save()
        resp = self.client.post(
            self.url,
            data={'email': self.email, 'password': self.password},
            content_type='application/json')
        result = resp.json()
        self.assertIn('access', result.keys())
        self.assertIn('refresh', result.keys())


class RefreshTokenTestCase(TestCase):
    client = APIClient()
    token_url = '/api/token/'
    url = '/api/token/refresh/'
    email = EMAIL
    password = PASSWD

    def test_api_token(self):
        user = baker.make(User, email=self.email)
        user.set_password(self.password)
        user.save()
        resp = self.client.post(
            self.token_url,
            data={'email': self.email, 'password': self.password},
            content_type='application/json')
        jwt = resp.json()
        resp = self.client.post(
            self.url,
            data={'refresh': jwt['refresh']},
            content_type='application/json')
        result = resp.json()
        self.assertIn('access', result.keys())