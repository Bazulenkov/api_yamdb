from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class YamUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Custom fields", {"fields": ("bio", "role")}),
    )
    list_display = UserAdmin.list_display + ("role",)
