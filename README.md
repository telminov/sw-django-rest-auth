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
    ...
]
```

add to settings.py TokenAuthentication method.
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}
```

## Client for authentication service
add to settings.py
```python
AUTH_SERVICE_CHECK_TOKEN_URL = 'https://.../check_token/'   # address for authentication service project
AUTH_TOKEN = '0f49bc20b02bc70b034bd9d6036c8155e00109eb'     # token for connecting to authentication service
```

view looks like
```python
from sw_rest_auth.authentication import TokenServiceAuthentication

@api_view(['GET'])
@authentication_classes((TokenServiceAuthentication))
@permission_classes((IsAuthenticated,))
def index(request):
    data = {
        'message': 'Hello, world!'
    }
    return Response(data)
```