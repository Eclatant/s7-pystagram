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

        self.urls = namedtuple('URL', (
            'create_post',
        ))(
            lambda : reverse('photos:create'),
            )

    def _login(self, username, password):
        return self.client.post(
            settings.LOGIN_URL, {'username': username, 'password': password}
        )

    def _add_post(self, data, follow=True):
        return self.client.post(
            self.urls.create_post(), data=data, follow=follow
        )

    def test_post(self):
        self._login(**self.users[0])
        _form_data = {
            'content': 'FSAD@3@#$!sdflkj content',
        }
        response = self._add_post(_form_data)
        self.assertEqual(response.status_code, 200)

    @unittest.skip('얘는 뭔가 이상해서 일단 패스;;;')
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

    @unittest.skip('얘는 뭔가 이상해서 일단 패스;;;')
    # 자신의 포스트틑 '좋아요' 누르면 안되는 테스트
    def test_fail_sameuser_post_and_like(self):
        post1 = Post.objects.filter(pk=1)
        likes = post1.like_set.all
        res = True
        for like in likes:
            if like.user == post1.user:
                res = False
        self.assertEqual(True, res)

    # 유저가 하나의 포스트에 중복 '좋아요'를 누르면 안되는 테스트
