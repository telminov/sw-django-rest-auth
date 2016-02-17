# coding: utf-8
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from . import models


class CheckToken(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        try:
            return Token.objects.get(key=value)
        except Token.DoesNotExist:
            raise serializers.ValidationError('Token not found')


class CheckPerm(serializers.Serializer):
    user = serializers.CharField()
    perm = serializers.CharField(max_length=50)

    def validate_user(self, value):
        try:
            return User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with username "{0}" not found'.format(value))

    def validate_perm(self, value):
        try:
            return models.Permission.objects.get(code=value)
        except models.Permission.DoesNotExist:
            raise serializers.ValidationError('Permission with code "{0}" not found'.format(value))

    def validate(self, attrs):
        user = attrs.get('user')
        perm = attrs.get('perm')
        if user and perm:
            try:
                models.UserPermission.objects.get(user=user, permission=perm)
            except models.UserPermission.DoesNotExist:
                raise serializers.ValidationError('User "{0}" have no permission with code "{1}"'.format(
                    user.username,
                    perm.code
                ))

        return attrs
