from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_active")
    # fieldsets = (
    #     (None, {"fields": ("username", "password")}),
    #     ("Personal info", {"fields": ("email")}),
    #     ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    #     ("Important dates", {"fields": ("last_login", "date_joined")}),
    # )


# Đăng ký custom User Admin
admin.site.register(CustomUser, CustomUserAdmin)
