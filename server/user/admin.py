from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


custom_fields = (
    (None, {'fields': ('avatar', 'role')}),
)

@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + custom_fields
    add_fieldsets = UserAdmin.add_fieldsets + custom_fields

