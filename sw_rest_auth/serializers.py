# coding: utf-8
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.backends import ModelBackend
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
            return AuthUser.objects.get(username=value)
        except AuthUser.DoesNotExist:
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
            user_qs = models.UserPermission.objects.filter(user=user, permission=perm)

            group_qs = models.GroupPermission.objects.filter(
                group__in=user.groups.all(),
                permission=perm
            )

            if not (user_qs.exists() or group_qs.exists()):
                raise serializers.ValidationError('User "{0}" have no permission with code "{1}"'.format(
                    user.username,
                    perm.code
                ))

        return attrs


class CheckLoginPassword(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def __init__(self, *args, request, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if password and password:
            is_correct = bool(ModelBackend().authenticate(self.request, username=username, password=password))
            if not is_correct:
                raise serializers.ValidationError('Incorrect login and password combination.')
        return attrs


class User(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        exclude = ('password', )
