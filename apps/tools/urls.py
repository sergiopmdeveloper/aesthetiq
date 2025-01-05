from django.urls import path

from apps.tools import views

urlpatterns = [
    path("remove-background", views.RemoveBackgroundView.as_view(), name="remove-background"),
    path(
        "save-remove-background-result",
        views.SaveRemoveBackgroundResultView.as_view(),
        name="save-remove-background-result",
    ),
]
