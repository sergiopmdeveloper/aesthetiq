from django.contrib import admin

from authentication.models import AppUser


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    """
    App user registration in the admin.
    """

    list_display = ("username", "email")
