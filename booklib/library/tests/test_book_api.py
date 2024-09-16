import string
import random

from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from library.models import Book, Author
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
        author = baker.make(Author)
        data = {'title': 'Something New', 'description': 'Hello guys', 'published_on': '2022-04-23', 'author': [author.uuid]}
        resp = self.client.post(self.url, data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()['title'], data['title'])
        self.assertEqual(resp.json()['description'], data['description'])
        self.assertEqual(resp.json()['published_on'], data['published_on'])

    def test_create_duplicate_title_book(self):
        author = baker.make(Author)
        title = 'This is new Book'
        baker.make(Book, title=title)
        data = {'title': title, 'description': 'Hello guys', 'published_on': '2022-04-23', 'author': [author.uuid]}
        resp = self.client.post(self.url, data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 400)
        content = resp.json()
        self.assertIn('title', content.keys())

    def test_put_api_book_not_exist(self):
        author = baker.make(Author)
        title = 'This is new Book'
        random_str = ''.join(random.sample(string.ascii_letters, 20))
        data = {'title': title, 'description': 'Welcome drinks', 'published_on': '2012-05-27', 'author': [author.uuid]}
        resp = self.client.put(f'{self.url}{random_str}/', data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 404)

    def test_book_put_api_with_empty_data(self):
        book = baker.make(Book)
        data = {}
        resp = self.client.put(f'{self.url}{book.uuid}/', data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 400)

    def test_book_patch_api_with_data(self):
        book = baker.make(Book)
        data = {'title': 'This is new Book Released'}
        resp = self.client.patch(f'{self.url}{book.uuid}/', data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['title'], data['title'])

    def test_book_delete_api(self):
        book = baker.make(Book)
        book_count = Book.objects.all().count()
        self.assertEqual(book_count, 1)
        resp = self.client.delete(f'{self.url}{book.uuid}/', headers=self.get_headers())
        self.assertEqual(resp.status_code, 204)
        book_count = Book.objects.all().count()
        self.assertEqual(book_count, 0)

    def test_put_api_book_with_updated_data_response(self):
        author = baker.make(Author)
        book = baker.make(Book, title='abc')
        data = {'title': 'XYZ', 'description': 'Welcome drinks', 'published_on': '2012-05-27', 'author': [author.uuid]}
        resp = self.client.put(f'{self.url}{book.uuid}/', data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['title'], data['title'])
        self.assertEqual(resp.json()['description'], data['description'])
        self.assertEqual(resp.json()['published_on'], data['published_on'])
