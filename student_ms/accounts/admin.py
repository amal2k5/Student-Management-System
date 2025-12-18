from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

admin.site.register(User)

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("email",)}),
        ("Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "role", "password1", "password2"),
        }),
    )

    list_display = ("username", "email", "role", "is_staff")
    search_fields = ("username", "email")
    ordering = ("username",)

admin.site.register(User, CustomUserAdmin)



