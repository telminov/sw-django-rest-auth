# coding: utf-8
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
import requests


class TokenServiceAuthentication(BaseAuthentication):
    """
    Token based authentication by means third part services.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "TokenService ".  For example:

        Authorization: TokenService 401f7ac837da42b97f613d789819ff93537bee6a
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'tokenservice':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token_key = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self._check_token(token_key)

    @staticmethod
    def _check_token(token_key):
        url = settings.AUTH_SERVICE_CHECK_TOKEN_URL
        auth_token = settings.AUTH_TOKEN
        auth_verified_ssl_crt = getattr(settings, 'AUTH_VERIFIED_SSL_CRT_PATH', None)

        headers = {'Authorization': 'Token %s' % auth_token}
        data = {'token': token_key}
        try:
            kwargs = {
                'headers': headers,
                'data': data,
            }
            kwargs['verify'] = auth_verified_ssl_crt
            r = requests.post(url, **kwargs)
        except requests.ConnectionError:
            raise exceptions.AuthenticationFailed('Invalid token header. ConnectionError.')

        if r.status_code == 200:
            result = r.json()
            username = result['username']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)
            return user, None

        elif r.status_code == 400:
            result = r.json()
            token_err_description = ', '.join(result['token'])
            raise exceptions.AuthenticationFailed('Invalid token header. %s' % token_err_description)

        else:
            raise exceptions.AuthenticationFailed('Invalid token header. Unknown error: %s' % r.text)

    def authenticate_header(self, request):
        return 'TokenService'
