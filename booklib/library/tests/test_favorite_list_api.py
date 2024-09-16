import random
import string

from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from library.models import Author, FavoriteBooks, Book
from users.models import User

EMAIL = 'abc@gmail.com'
PASSWD = 'random_string@$&123'


class FavoriteBookAPITestCase(TestCase):
    client = APIClient()
    login_url = '/login/'
    url = '/fav-book/'
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

    def test_favorite_book_list_api(self):
        books = baker.make(Book, _quantity=4)
        for bk in books:
            baker.make(FavoriteBooks, user=self.user, book=bk)
        resp = self.client.get(self.url, headers=self.get_headers())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['count'], 4)

    def test_favorite_book_create_api_with_empty_data(self):
        data = {}
        resp = self.client.post(self.url, data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 400)

    def test_favorite_book_create_api_with_valid_data(self):
        book = baker.make(Book)
        data = {'book_uuid': str(book.uuid)}
        resp = self.client.post(self.url, data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 201)
        fav_count = FavoriteBooks.objects.filter(user=self.user).count()
        self.assertEqual(fav_count, 1)

    def test_favorite_book_create_api_limit_check(self):
        books = baker.make(Book, _quantity=20)
        for bk in books:
            baker.make(FavoriteBooks, user=self.user, book=bk)
        new_bk = baker.make(Book)
        data = {'book_uuid': str(new_bk.uuid)}
        resp = self.client.post(self.url, data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 400)
        self.assertIn('book', resp.json().keys())

    def test_favorite_book_put_api(self):
        book = baker.make(Book)
        fv = baker.make(FavoriteBooks, user=self.user, book=book)
        data = {'book_uuid': str(book.uuid)}
        resp = self.client.put(f'{self.url}{str(fv.uuid)}/', data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 405)

    def test_favorite_book_patch_api(self):
        book = baker.make(Book)
        fv = baker.make(FavoriteBooks, user=self.user, book=book)
        data = {'book_uuid': str(book.uuid)}
        resp = self.client.put(f'{self.url}{str(fv.uuid)}/', data=data, content_type='application/json', headers=self.get_headers())
        self.assertEqual(resp.status_code, 405)

    def test_favorite_book_delete_api(self):
        book = baker.make(Book)
        fv = baker.make(FavoriteBooks, user=self.user, book=book)
        resp = self.client.delete(f'{self.url}{str(fv.uuid)}/', headers=self.get_headers())
        self.assertEqual(resp.status_code, 204)

    def test_favorite_book_delete_for_no_entry(self):
        book = baker.make(Book)
        fv = baker.make(FavoriteBooks, user=self.user, book=book)
        random_str = ''.join(random.sample(string.ascii_letters, 20))
        resp = self.client.delete(f'{self.url}{random_str}/', headers=self.get_headers())
        self.assertEqual(resp.status_code, 404)