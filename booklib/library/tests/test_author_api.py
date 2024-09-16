from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from library.models import Author
from users.models import User

EMAIL = 'abc@gmail.com'
PASSWD = 'random_string@$&123'


class AuthorAPIAdminUserTestCase(TestCase):
    client = APIClient()
    login_url = '/login/'
    url = '/authors/'
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

    def test_author_create_api_with_empty_data(self):
        data = {}
        resp = self.client.post(self.url, data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 400)

    def test_author_create_api_with_valid_data(self):
        data = {'name': 'Something New', 'description': 'Hello guys'}
        resp = self.client.post(self.url, data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()['name'], data['name'])
        self.assertEqual(resp.json()['description'], data['description'])

    def test_author_create_with_duplicate_name(self):
        name = "ramesh dai ji"
        baker.make(Author, name=name)
        data = {'name': name, 'description': 'Hello guys'}
        resp = self.client.post(self.url, data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 400)
        self.assertIn('name', resp.json().keys())

    def test_author_delete_api(self):
        author = baker.make(Author, name='jpt boy')
        self.assertEqual(Author.objects.filter(is_deleted=False).count(), 1)
        resp = self.client.delete(f'{self.url}{author.uuid}/', headers=self.get_headers())
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Author.objects.filter(is_deleted=False).count(), 0)
        self.assertEqual(Author.objects.filter(is_deleted=True).count(), 1)

    def test_author_put_api(self):
        author = baker.make(Author, name="random name")
        data = {'name': "new boy name", 'description': 'Hello guys'}
        resp = self.client.put(f'{self.url}{author.uuid}/', data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['name'], data['name'])
        self.assertEqual(resp.json()['description'], data['description'])

    def test_author_patch_api(self):
        author = baker.make(Author, name="random name")
        data = {'name': "new boy name", 'description': 'Hello guys'}
        resp = self.client.patch(f'{self.url}{author.uuid}/', data=data, content_type='application/json',
                               headers=self.get_headers())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['name'], data['name'])
        self.assertEqual(resp.json()['description'], data['description'])

    def test_author_list_api(self):
        count = 4
        baker.make(Author, _quantity=count)
        resp = self.client.get(self.url, headers=self.get_headers())
        self.assertEqual(resp.json()['count'], count)

