# coding: utf-8
import requests
from django.conf import settings
from django.contrib.auth.models import User


class RestBackend(object):
    def authenticate(self, username, password):
        url = settings.AUTH_SERVICE_CHECK_LOGIN_PASSWORD_URL
        auth_token = settings.AUTH_TOKEN
        auth_verified_ssl_crt = getattr(settings, 'AUTH_VERIFIED_SSL_CRT_PATH', None)

        headers = {'Authorization': 'Token %s' % auth_token}
        data = {'username': username, 'password': password}
        try:
            kwargs = {
                'headers': headers,
                'data': data,
            }
            kwargs['verify'] = auth_verified_ssl_crt
            r = requests.post(url, **kwargs)
        except requests.ConnectionError:
            return None

        if r.status_code == 200:
            result = r.json()
            result.pop('id')
            result.pop('user_permissions')
            result.pop('groups')
            try:
                user = User.objects.get(username=result['username'])
            except User.DoesNotExist:
                result['password'] = password
                user = User.objects.create_user(**result)
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def has_perm(self, user, perm, obj):
        from .permissions import CodePermission
        return CodePermission.has_permission_by_params(user.username, perm, raise_exception=False)
