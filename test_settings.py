ROOT_URLCONF = 'sw_rest_auth.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'rest_framework.authtoken',
    'sw_rest_auth',
]

SECRET_KEY = "123"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

AUTH_SERVICE_CHECK_TOKEN_URL = 'https://auth-service/check_token/'
AUTH_SERVICE_CHECK_PERM_URL = 'https://auth-service/check_perm/'
AUTH_TOKEN = '321'
