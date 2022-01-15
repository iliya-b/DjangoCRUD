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
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)
    teams = models.ManyToManyField('Team')

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
        return "User (%s) %s %s %s" % (self.telegram_id, self.name, 'active' if self.is_active else 'inactive', 'blocked' if self.is_blocked else '')


class Team(models.Model):
    name = models.CharField('Name', max_length=100, null=False, unique=True)
    password = models.CharField(max_length=255, null=False, unique=True)
    admin = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Team %s (%d)" % (self.name, self.id)

    class Meta:
        verbose_name_plural = 'Teams'


class Pair(models.Model):
    user_a = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='+')
    user_b = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='+')
    about = models.TextField(null=True)
    feedback_a = models.TextField(null=True)
    feedback_b = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
