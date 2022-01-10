from django.contrib import admin
from .models import User, Pair, Team


# Here we register models to show in admin panel

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'name', 'is_active', 'email')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    description = "Team"
    list_display = ('name',)
