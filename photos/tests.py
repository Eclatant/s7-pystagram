import unittest
from collections import namedtuple

from django.test import TestCase
from django.test import Client
from django.db import transaction
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.conf import settings

from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve

from . models import Post, Comment, Like
from . import views, models, forms


User = get_user_model()

class LikeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.users = (
            {'username': 'test1', 'password': 'asdf'},
            {'username': 'test2', 'password': 'asdf'},
        )
        for _user in self.users:
            User.objects.create_user(**_user)

    def _login(self, username, password):
        return self.client.post(
            settings.LOGIN_URL, {'username': username, 'password': password}
        )

    def test_other_user_url(self): # 유저링크를 누르면 '/phtos/user_name' 이런식의 url 이 만들어져야한다
        """self._login(**self.users[0])
        form_data = {
            'content': 'blah blah',
        }
        response = self._add_post(form_data)
        print(response.context)
        self.assertEqual(response.status_code, 200)
        self.client.post(self.urls.create_photo(), data=data, follow=follow)"""
