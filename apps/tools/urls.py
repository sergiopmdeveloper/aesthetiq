from django.urls import path

from apps.tools import views

urlpatterns = [
    path("remove-background", views.RemoveBackgroundView.as_view(), name="remove-background"),
]
