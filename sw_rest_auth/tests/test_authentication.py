# coding: utf-8
import requests
from django.test import mock
from django.contrib.auth.models import User
from rest_framework import test, status
from rest_framework.authtoken.models import Token
from .. import authentication


class AuthenticationTestCase(test.APITestCase):

    def setUp(self):
        user = User.objects.create(username='tester')
        token = Token.objects.create(user=user)
        self.header = {'HTTP_AUTHORIZATION': 'TokenService ' + token.key}
        self.request_factory = test.APIRequestFactory()
        self.request = self.request_factory.get('/some_url/', **self.header)

    @mock.patch('sw_rest_auth.authentication.requests')
    def test_success_request(self, requests_mock):
        requests_mock.post.return_value.status_code = status.HTTP_200_OK
        requests_mock.post.return_value.json.return_value = {'username': 'test_username'}

        user, _ = authentication.TokenServiceAuthentication().authenticate(self.request)

        self.assertTrue(requests_mock.post.called)
        self.assertEqual(user.username, requests_mock.post.return_value.json.return_value['username'])

    @mock.patch('sw_rest_auth.authentication.requests')
    def test_validation_error(self, requests_mock):
        requests_mock.post.return_value.status_code = status.HTTP_400_BAD_REQUEST
        requests_mock.post.return_value.json.return_value = {'token': 'token error'}

        auth_ex = None
        try:
            authentication.TokenServiceAuthentication().authenticate(self.request)
        except authentication.exceptions.AuthenticationFailed as ex:
            auth_ex = ex

        self.assertTrue(requests_mock.post.called)
        self.assertIsNotNone(auth_ex)

    @mock.patch('sw_rest_auth.authentication.requests')
    def test_connection_error(self, requests_mock):
        requests_mock.post.return_value.side_effect = requests.ConnectionError('Error')

        auth_ex = None
        try:
            authentication.TokenServiceAuthentication().authenticate(self.request)
        except authentication.exceptions.AuthenticationFailed as ex:
            auth_ex = ex

        self.assertTrue(requests_mock.post.called)
        self.assertIsNotNone(auth_ex)

