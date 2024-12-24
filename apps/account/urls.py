from django.urls import path

from apps.account import views

urlpatterns = [
    path("details", views.AccountDetailsView.as_view(), name="account-details"),
]
