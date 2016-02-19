# coding: utf-8
from django.conf import settings
from rest_framework import permissions
import requests


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
            return False

        return r.status_code == 200

    @classmethod
    def decorate(cls, code):
        def decorator():
            return cls(permission_code=code)
        return decorator
