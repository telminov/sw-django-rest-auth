# coding: utf-8
from django.test import mock
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import test, status


class AuthHelperMixin(object):

    def setUp(self):
        super(AuthHelperMixin, self).setUp()
        self.requests_patcher = mock.patch('sw_rest_auth.permissions.requests')
        self.requests_mock = self.requests_patcher.start()

    def tearDown(self):
        super(AuthHelperMixin, self).tearDown()
        self.requests_mock.stop()

    def assertPermChecked(self, user, perm):
        self.assertTrue(self.requests_mock.get.called)
        call_args, call_kwargs = self.requests_mock.get.call_args
        self.assertEqual(settings.AUTH_SERVICE_CHECK_PERM_URL, call_args[0])
        self.assertEqual(user.username, call_kwargs['params']['user'])
        self.assertEqual(perm, call_kwargs['params']['perm'])

    def force_permission(self, user=None, perm=None, perm_list=None):
        if not perm_list and perm:
            perm_list = [perm]

        def side_effect(url, headers, params, verify):
            response_mock = mock.Mock()
            if params['user'] == user.username and params['perm'] in perm_list:
                response_mock.status_code = status.HTTP_200_OK
            else:
                response_mock.status_code = status.HTTP_400_BAD_REQUEST
            return response_mock

        if user and perm_list:
            self.requests_mock.get.side_effect = side_effect
        else:
            self.requests_mock.get.side_effect = None


class AuthTestCaseMixin(AuthHelperMixin):
    url = None
    perm = None
    method_name = 'post'

    def get_method_names(self):
        if self.get_perm_map():
            return self.get_perm_map().keys()
        else:
            return [self.method_name]

    def get_perm_map(self):
        if self.perm:
            return {self.method_name: self.perm}
        else:
            return None

    def setUp(self):
        super(AuthTestCaseMixin, self).setUp()
        self.client.force_authenticate(self.get_user())
        if self.get_perm_map():
            self.force_permission(self.get_user(), perm_list=self.get_perm_map().values())

    def test_not_auth(self):
        self.client.force_authenticate()         # unset authentication
        for method_name in self.get_method_names():
            response = getattr(self.client, method_name)(self.url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_forbidden(self):
        if not self.get_perm_map():
            return

        self.client.force_authenticate(user=self.get_user())
        self.force_permission()     # unset permission
        for method_name, perm_code in self.get_perm_map().items():
            response = getattr(self.client, method_name)(self.url)
            self.assertPermChecked(self.get_user(), perm_code)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_perm(self):
        if not self.get_perm_map():
            return

        self.client.force_authenticate(self.get_user())
        for method_name, perm_code in self.get_perm_map().items():
            self.force_permission(self.get_user(), perm=perm_code)
            response = getattr(self.client, method_name)(self.url)
            self.assertPermChecked(self.get_user(), perm_code)
            self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def get_user(self):
        if not hasattr(self, 'user') or not self.user:
            self.user = User.objects.create(username='tester')
        return self.user

