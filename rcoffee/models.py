from datetime import datetime
from django.utils.translation import gettext as _
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
    companies = models.ManyToManyField('Company')

    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    admins = AdminsManager()

    def __repr__(self):
        return (f'{self.name}\n'
                f'*{_("Profile")}:* {self.link}\n\n'
                f'*{_("Work")}:* {self.work}\n'
                f'*{_("About")}:* {self.about}\n\n'
                f'{_("Write to your partner telegram")} – [{self.name}](tg://user?id={self.telegram_id})')

    def __str__(self):
        return "User %s (%d)" % (self.name, self.id)


class Company(models.Model):
    name = models.CharField('Name', max_length=100, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    admin = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Company %s (%d)" % (self.name, self.id)

    class Meta:
        verbose_name_plural = 'Companies'


class Pair(models.Model):
    user_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    user_b = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    about = models.TextField()

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
