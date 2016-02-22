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


class CheckPerm(AuthTestCaseMixin, test.APITestCase):
    url = reverse(views.check_perm)

    def setUp(self):
        super(CheckPerm, self).setUp()
        self.permission = models.Permission.objects.create(code='code', name='name', description='description')

    def test_have_perm(self):
        models.UserPermission.objects.create(permission=self.permission, user=self.get_user())
        response = self.client.get(self.url, {'user': self.get_user().username, 'perm': self.permission.code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_have_no_perm(self):
        models.UserPermission.objects.filter(permission=self.permission, user=self.get_user()).delete()
        response = self.client.get(self.url, {'user': self.get_user().username, 'perm': self.permission.code})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
