# coding: utf-8
from django.db import models
from django.contrib.auth.models import User


class Permission(models.Model):
    code = models.CharField(max_length=50, unique=True, help_text='code for using in permission class in program code')
    name = models.CharField(max_length=100, unique=True, help_text='human permission name')
    description = models.TextField(blank=True, help_text='detailed description')

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.code)


class UserPermission(models.Model):
    user = models.ForeignKey(User)
    permission = models.ForeignKey(Permission)

    class Meta:
        unique_together = ('user', 'permission')

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.permission)
