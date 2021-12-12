import json
import os

from django.http import SimpleCookie
from django.test import TestCase
from django.test import Client
import sys
from rest_framework import status
from reducer.models import Users, Domain, URLs


BASE_DIR = os.getcwd()
path_to_domains = os.path.join(BASE_DIR, 'reducer', 'management', 'commands')
sys.path.append(path_to_domains)

import ensure_domains

c = Client()

test_url = {'url_destination': 'www.ya.ru',
            'domain': 1}

test_custom_url = {'url_destination': 'www.vk.ru',
                   'domain': 2,
                   'url': 'vk_anton'}


class ReducerTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        domains = ensure_domains.Command()
        domains.handle()
        c.cookies = SimpleCookie({'dp_test_user_id': '1111111111111111111'})

    def setUp(self):
        domain = Domain.objects.get(domain='domain1.link')
        user = Users(user_uuid='1111111111111111111')
        user.save()

        url = URLs(domain=domain,
                   url='test_redirect',
                   url_destination='ya.ru',
                   user_uuid=user)
        url.save()

    def test_get_urls(self):
        response = c.get('/url_reducer/get_url/page=0')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_urls(self):
        response = c.post('/url_reducer/set_url', test_url)
        self.url = json.loads(response.content)['url']
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_custom_urls(self):
        response = c.post('/url_reducer/set_url', test_custom_url)
        self.url = json.loads(response.content)['url']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         {'res': 'url_created',
                          'url': 'dom123.com/vk_anton'}
                         )

    def test_get_redirect(self):
        response = c.get(f'/url_reducer/redirect/domain1.link/test_redirect')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_delete_url(self):
        r = c.delete(f'/url_reducer/delete_url/1')
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def tearDown(self):
        pass

