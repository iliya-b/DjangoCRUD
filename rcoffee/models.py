from django.db import models
from django.db.models import Model


class AdminsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)


class User(models.Model):
    telegram_id = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    work = models.TextField()
    about = models.TextField()
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    admins = AdminsManager()
    object = models.Manager()

class Pair(models.Model):
    user_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    user_b = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    about = models.TextField()

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
