from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from library.models import Book
from users.models import User

EMAIL = 'abc@gmail.com'
PASSWD = 'random_string@$&123'


class BookAPINormalUserTestCase(TestCase):
    client = APIClient()
    login_url = '/login/'
    url = '/book/'
    access_token = ''

    def setUp(self):
        self.user = baker.make(User, email=EMAIL)
        self.user.set_password(PASSWD)
        self.user.save()
        data = {'email': EMAIL, 'password': PASSWD}
        resp = self.client.post(self.login_url, data=data, content_type='application/json').json()
        self.access_token = resp['access']

    def get_headers(self):
        return {'Authorization': 'Bearer {}'.format(self.access_token)}

    def test_book_create_api_by_normal_user(self):
        data = {}
        resp = self.client.post(self.url, data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 403)

    def test_book_put_api_by_normal_user(self):
        book = baker.make(Book)
        data = {'name': 'Old is Gold'}
        resp = self.client.put(f'{self.url}{book.uuid}/', data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 403)

    def test_book_patch_api_by_normal_user(self):
        book = baker.make(Book)
        data = {'name': 'Old is Gold'}
        resp = self.client.patch(f'{self.url}{book.uuid}/', data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 403)

    def test_book_delete_api_by_normal_user(self):
        book = baker.make(Book)
        resp = self.client.delete(f'{self.url}{book.uuid}/', content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 403)


class BookAPIAdminUserTestCase(TestCase):
    client = APIClient()
    login_url = '/login/'
    url = '/book/'
    access_token = ''

    def setUp(self):
        self.user = baker.make(User, email=EMAIL, is_staff=True)
        self.user.set_password(PASSWD)
        self.user.save()
        data = {'email': EMAIL, 'password': PASSWD}
        resp = self.client.post(self.login_url, data=data, content_type='application/json').json()
        self.access_token = resp['access']

    def get_headers(self):
        return {'Authorization': 'Bearer {}'.format(self.access_token)}

    def test_book_create_api_with_empty_data(self):
        data = {}
        resp = self.client.post(self.url, data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 400)

    def test_book_create_api_with_valid_data(self):
        data = {'title': 'Something New', 'description': 'Hello guys', 'published_on': '2022-04-23'}
        resp = self.client.post(self.url, data=data, content_type='application/json', headers=self.get_headers())
        print(resp.status_code)
        print(resp.json())

    # def test_create_duplicate_title_book(self):
    #     title = 'This is new Book'
    #     baker.make(Book, title=title)
    #     data = {'title': title}
    #     resp = self.client.post(self.url, data=data, content_type='application/json', headers=self.get_headers())
    #     self.assertEqual(resp.status_code, 400)
    #
    # def test_book_put_api_with_empty_data(self):
    #     book = baker.make(Book)
    #     data = {}
    #     resp = self.client.put(f'{self.url}{book.uuid}/', data=data, content_type='application/json', headers=self.get_headers())
    #     self.assertEqual(resp.status_code, 404)

