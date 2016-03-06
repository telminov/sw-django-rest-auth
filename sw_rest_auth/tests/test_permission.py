# coding: utf-8
import requests
from django.conf import settings
from django.test import mock
from django.contrib.auth.models import User
from rest_framework import test, status
from rest_framework.exceptions import PermissionDenied
from .. import permissions


class PermissionTestCase(test.APITestCase):

    def setUp(self):
        self.request_factory = test.APIRequestFactory()
        self.request = self.request_factory.get('/some_url/')
        self.request.user = User.objects.create(username='tester')

    @mock.patch('sw_rest_auth.permissions.requests')
    def test_success_request(self, requests_mock):
        requests_mock.get.return_value.status_code = status.HTTP_200_OK

        perm_code = 'TEST_CODE'
        perm = permissions.CodePermission.decorate(perm_code)()
        has_permission = perm.has_permission(self.request, mock.Mock())
        self.assertTrue(has_permission)

        call_args, call_kwargs = requests_mock.get.call_args
        self.assertEqual(settings.AUTH_SERVICE_CHECK_PERM_URL, call_args[0])
        self.assertEqual(self.request.user.username, call_kwargs['params']['user'])
        self.assertEqual(perm_code, call_kwargs['params']['perm'])

    @mock.patch('sw_rest_auth.permissions.requests')
    def test_validation_error(self, requests_mock):
        requests_mock.get.return_value.status_code = status.HTTP_400_BAD_REQUEST

        perm_code = 'TEST_CODE'
        perm = permissions.CodePermission.decorate(perm_code)()

        exception = None
        try:
            perm.has_permission(self.request, mock.Mock())
        except PermissionDenied as ex:
            exception = ex
        self.assertTrue(exception)

    @mock.patch('sw_rest_auth.permissions.requests.head', side_effect=requests.ConnectionError)
    def test_connection_error(self, requests_mock):
        perm_code = 'TEST_CODE'
        perm = permissions.CodePermission.decorate(perm_code)()

        exception = None
        try:
            perm.has_permission(self.request, mock.Mock())
        except PermissionDenied as ex:
            exception = ex
        self.assertTrue(exception)
