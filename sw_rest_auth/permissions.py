# coding: utf-8
from django.conf import settings
from rest_framework import permissions
import requests
from rest_framework.exceptions import PermissionDenied


class CodePermission(permissions.BasePermission):
    def __init__(self, permission_code):
        super(CodePermission, self).__init__()
        self.permission_code = permission_code

    def has_permission(self, request, view):
        if not (request.user and request.user.username):
            return False

        url = settings.AUTH_SERVICE_CHECK_PERM_URL
        auth_token = settings.AUTH_TOKEN
        auth_verified_ssl_crt = getattr(settings, 'AUTH_VERIFIED_SSL_CRT_PATH', None)

        headers = {'Authorization': 'Token %s' % auth_token}
        params = {'user': request.user.username, 'perm': self.permission_code}
        try:
            kwargs = {
                'headers': headers,
                'params': params,
            }
            if auth_verified_ssl_crt:
                kwargs['verify'] = auth_verified_ssl_crt
            r = requests.get(url, **kwargs)
        except requests.ConnectionError:
            raise PermissionDenied(detail='Can not connect to authorization service')

        if r.status_code != 200:
            detail = '; '.join(['%s: %s' % (k, ', '.join(v)) for k, v in r.json().items()])
            raise PermissionDenied(detail=detail)

        return True

    @classmethod
    def decorate(cls, code):
        def decorator():
            return cls(permission_code=code)
        return decorator
