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
        url = settings.AUTH_SERVICE_CHECK_PERM_URL
        auth_token = settings.AUTH_TOKEN

        headers = {'Authorization': 'Token %s' % auth_token}
        params = {'user': request.user.username, 'perm': self.permission_code}
        try:
            r = requests.get(url, headers=headers, params=params)
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
