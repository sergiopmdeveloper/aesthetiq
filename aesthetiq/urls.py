from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("authentication/", include("authentication.urls")),
    path("account/", include("apps.account.urls")),
]
