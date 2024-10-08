from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "is_staff", "is_active")


User = get_user_model()

admin.site.register(User, CustomUserAdmin)
