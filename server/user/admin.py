from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ( (None, {'fields': ('avatar',)}), )
    add_fieldsets = UserAdmin.add_fieldsets + ( (None, {'fields': ('avatar',)}), )

