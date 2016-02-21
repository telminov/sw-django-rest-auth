# coding: utf-8
# python setup.py sdist register upload
from distutils.core import setup

setup(
    name='sw-django-rest-auth',
    version='0.0.4',
    description='Soft Way company django restfromework authentication service package.',
    author='Telminov Sergey',
    url='https://github.com/telminov/sw-django-rest-auth',
    packages=[
        'sw_rest_auth',
        'sw_rest_auth.migrations',
    ],
    license='The MIT License',
    install_requires=[
        'django',
        'djangorestframework',
        'requests',
    ],
)