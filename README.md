# sw-django-rest-auth

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
    url(r'^check_perm/', sw_rest_auth.views.check_perm),
    ...
]
```

add to settings.py TokenAuthentication method.
```python
INSTALLED_APPS = [
    ...
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
