# coding: utf-8
# python setup.py sdist register upload
from setuptools import setup

setup(
    name='sw-django-rest-auth',
    version='0.0.17',
    description='Soft Way company django restfromework authentication service package.',
    author='Telminov Sergey',
    url='https://github.com/telminov/sw-django-rest-auth',
    packages=[
        'sw_rest_auth',
        'sw_rest_auth/migrations',
        'sw_rest_auth/tests',
    ],
    include_package_data=True,
    license='The MIT License',
    test_suite='runtests.runtests',
    install_requires=[
        'django',
        'djangorestframework',
        'requests',
    ],
)