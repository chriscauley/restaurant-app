from django.contrib import admin
from .models import User, Restaurant, Meal, Order, OrderItem
from django.contrib.auth.admin import UserAdmin


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    pass


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ( (None, {'fields': ('avatar',)}), )
    add_fieldsets = UserAdmin.add_fieldsets + ( (None, {'fields': ('avatar',)}), )

