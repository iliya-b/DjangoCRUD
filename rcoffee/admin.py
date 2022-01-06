from django.contrib import admin
from .models import User, Pair


# Here we register models to show in admin panel

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'name', 'is_verified', 'is_active', 'email')

