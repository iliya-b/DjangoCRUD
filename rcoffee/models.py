from datetime import datetime

from django.db import models
from django.db.models import Model


class AdminsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)


class User(models.Model):
    telegram_id = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    name = models.CharField('Name', max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)
    work = models.TextField(blank=True)
    about = models.TextField(blank=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    admins = AdminsManager()

    def __repr__(self):
        return (f'{self.name}\n'
                f'*Профиль:* {self.link}\n\n'
                f'*Чем занимается:* {self.work}\n'
                f'*Зацепки для начала разговора:* {self.about}\n\n'
                f'Напиши собеседнику в Telegram – [{self.name}](tg://user?id={self.telegram_id})')


class Pair(models.Model):
    user_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    user_b = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    about = models.TextField()

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
