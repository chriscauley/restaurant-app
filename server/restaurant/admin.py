from django.contrib import admin
from .models import Restaurant, MenuItem, MenuSection, Order, OrderItem
from django.contrib.auth.admin import UserAdmin


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    pass


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    pass


@admin.register(MenuSection)
class MenuSectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass
