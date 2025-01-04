from django.contrib import admin

from apps.tools.models import BackgroundRemoverResult


@admin.register(BackgroundRemoverResult)
class BackgroundRemoverResultAdmin(admin.ModelAdmin):
    """
    Background remover result registration in the admin.
    """

    list_display = ("user", "result_name")
