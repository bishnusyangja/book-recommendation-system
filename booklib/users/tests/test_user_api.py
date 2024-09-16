from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker
from users.models import User


class RegistrationAPITestCase(TestCase):
    client = APIClient()
    url = '/register/'

    def test_user_register_with_empty_data(self):
        data = {}
        resp = self.client.post(self.url, data=data, content_type='application/json')
        print(resp.json())
        self.assertEqual(resp.status_code, 400)

    def test_user_registration_with_valid_data(self):
        data  = {}
        # check is_active

    def test_duplicate_email_registration(self):
        email = ''
        # baker.make(User, email=email)
        # data = {'email': email}