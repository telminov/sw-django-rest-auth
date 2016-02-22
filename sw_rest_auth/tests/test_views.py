# coding: utf-8
from django.core.urlresolvers import reverse
from django.test import mock
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import test, status
from rest_framework.authtoken.models import Token
from .. import models
from .. import views
from .helpers import AuthTestCaseMixin


class CheckToken(AuthTestCaseMixin, test.APITestCase):
    url = reverse(views.check_token)

    def test_success(self):
        token = Token.objects.create(user=self.get_user())
        response = self.client.post(self.url, {'token': token.key})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], token.user.username)

    def test_invalid_key(self):
        response = self.client.post(self.url, {'token': 'not_existing_token_key'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
