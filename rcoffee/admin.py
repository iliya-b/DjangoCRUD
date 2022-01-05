from django.contrib import admin

from .models import User, Pair

for entity in (User, Pair):
    admin.site.register(entity)

