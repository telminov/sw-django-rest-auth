# coding: utf-8
from django.contrib import admin
from . import models

admin.site.register(models.Permission)
admin.site.register(models.UserPermission)
admin.site.register(models.GroupPermission)
