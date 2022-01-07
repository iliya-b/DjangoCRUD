from django.contrib import admin
from .models import User, Pair, Company


# Here we register models to show in admin panel

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'name', 'is_verified', 'is_active', 'email')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    description = "Company"
    list_display = ('name',)

