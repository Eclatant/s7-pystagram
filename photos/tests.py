import unittest
from collections import namedtuple

from django.test import TestCase
from django.test import Client
from django.db import transaction
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.conf import settings

from django.core.urlresolvers import reverse

from . import views

from . models import Post, Like

class LikeTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_craete_post(self):
        self.client.post(settings.LOGIN_URL, {'username': 'hello1', 'password': 'asdf'})
        form_data = {
            'content':'blah blah',
        }
        url = reverse('photos:create')
        response = self.client.post(url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_add_like(self):
        response = self.client.post(settings.LOGIN_URL, {'username': 'hello1', 'password': 'asdf'})
        form_data = {
            'content':'blah blah',
        }
        url = reverse('photos:create')
        response = self.client.post(url, form_data, follow=True)
        add_like_url = reverse('photos:add_like', args=[28])
        response = self.client.post(add_like_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/login/?next=/photos/posts/28/add_like/')
    # 테스트 코드만드는데 수업시간에 했던거 하나도 기억이안나효 븅진인가봐요 ㅠㅠ
    # 아재라서 코딩 피지컬이 딸리는거같아요 오버워치도 심해에서 못벗어나고있어요 대학생애들이 힐러만하래요 서럽... 
