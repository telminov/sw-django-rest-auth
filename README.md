# sw-django-rest-auth
[![Build Status](https://travis-ci.org/telminov/sw-django-rest-auth.svg?branch=master)](https://travis-ci.org/telminov/sw-django-rest-auth)
[![Coverage Status](https://coveralls.io/repos/github/telminov/sw-django-rest-auth/badge.svg?branch=master)](https://coveralls.io/github/telminov/sw-django-rest-auth?branch=master)
[![pypi-version](https://img.shields.io/pypi/v/sw-django-rest-auth.svg)](https://pypi.python.org/pypi/sw-django-rest-auth)


Package for creating separate authentication service
and using one in other services via rest_framework authentication classes mechanism.

## Install
```
pip install sw-django-rest-auth
```

## Authentication service
add to urls.py
```python
import sw_rest_auth.views

urlpatterns = [
    ...
    url(r'^check_token/', sw_rest_auth.views.check_token),
    url(r'^check_login_password/', sw_rest_auth.views.check_login_password),
    url(r'^check_perm/', sw_rest_auth.views.check_perm),
    ...
]
```

add to settings.py TokenAuthentication method.
```python
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken',
    'sw_rest_auth',
    ...
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}
```
You can generate token using [obtain_auth_token view](http://www.django-rest-framework.org/api-guide/authentication/#generating-tokens)

## Client for authentication service
### Authentication
add to settings.py
```python
AUTH_SERVICE_CHECK_TOKEN_URL = 'https://.../check_token/'   # address for authentication service project
AUTH_TOKEN = '0f49bc20b02bc70b034bd9d6036c8155e00109eb'     # token for connecting to authentication service
AUTH_VERIFIED_SSL_CRT_PATH = '/etc/ssl/myCompanyCA.crt'     # optional path to auth service server ssl-certificate

# for using service as auth backend for standard django authentication
AUTHENTICATION_BACKENDS = ['sw_rest_auth.auth_backends.RestBackend']
AUTH_SERVICE_CHECK_LOGIN_PASSWORD_URL = 'http://127.0.0.1:8000/check_login_password/'
```

Add TokenServiceAuthentication to authentication_classes. For example:
```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from sw_rest_auth.authentication import TokenServiceAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes((TokenServiceAuthentication,))
@permission_classes((IsAuthenticated,))
def index(request):
    data = {
        'message': 'Hello, world!'
    }
    return Response(data)
```

### Authorizing
add to settings.py
```python
AUTH_SERVICE_CHECK_PERM_URL = 'https://.../check_perm/'
```

Add CodePermission to view permissions class. For example:
```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from sw_rest_auth.authentication import TokenServiceAuthentication
from sw_rest_auth.permissions import CodePermission

@api_view(['GET'])
@authentication_classes((TokenServiceAuthentication,))
@permission_classes((CodePermission.decorate(code='CAN_READ_SECRET_DATA'),))
def index(request):
    data = {
        'message': 'Hello, world!'
    }
    return Response(data)

```

Don't forget add permissions and permission-user relations in authentication service database
(by means admin interface, for example).

### Requesting
Request to resourse under TokenServiceAuthentication protecting must have header "Authorization" with value starting with "TokenService " and authorized at service token. For example:
```
TokenService 213fe72ffb54e6c83194ec591fb364c3f897ed12
```
