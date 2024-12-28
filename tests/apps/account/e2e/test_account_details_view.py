import pytest
from django.urls import reverse

from apps.account.forms import AccountDetailsForm
from authentication.models import AppUser


@pytest.mark.django_db
def test_account_details_view_get_method_authenticated_session(client):
    """
    GIVEN an authenticated session
    WHEN a GET request is made to the account details view
    THEN render the account details page
    """

    # Arrange
    user_data = {"username": "username", "email": "user@email.com", "password": "password"}
    user = AppUser.objects.create_user(**user_data)
    client.force_login(user)

    # Act
    response = client.get(reverse("account-details"))
    templates = [template.name for template in response.templates]

    # Assert
    assert "account/account-details.html" in templates


def test_account_details_view_get_method_unauthenticated_session(client):
    """
    GIVEN an unauthenticated session
    WHEN a GET request is made to the account details view
    THEN redirect to the sign in page
    """

    # Act
    response = client.get(reverse("account-details"))

    # Assert
    assert response.status_code == 302
    assert response.url == reverse("sign-in") + f"?next={reverse('account-details')}"


@pytest.mark.parametrize(
    "first_name, last_name, expected_errors",
    [
        (
            "invalid_first_name",
            "invalid_last_name",
            {
                "first_name": ["Only letters and spaces are allowed."],
                "last_name": ["Only letters and spaces are allowed."],
            },
        ),
    ],
)
@pytest.mark.django_db
def test_account_details_view_post_method_invalid_data(
    client, first_name, last_name, expected_errors
):
    """
    GIVEN account details invalid data
    WHEN a POST request is made to the account details view
    THEN render the account details page with the form errors
    """

    # Arrange
    user_name_fields = {"first_name": first_name, "last_name": last_name}
    user_data = {"username": "username", "email": "user@email.com", "password": "password"}
    user = AppUser.objects.create_user(**user_data)
    client.force_login(user)

    # Act
    response = client.post(reverse("account-details"), user_name_fields)
    account_det_form: AccountDetailsForm = response.context["form"]
    rendered_templates = [template.name for template in response.templates]

    # Assert
    assert not account_det_form.is_valid()
    assert all(account_det_form.errors[field] == error for field, error in expected_errors.items())
    assert "account/account-details.html" in rendered_templates


@pytest.mark.django_db
def test_account_details_view_post_method_valid_data(client):
    """
    GIVEN account details valid data
    WHEN a POST request is made to the account details view
    THEN update the user details and render the account details page with a success message
    """

    # Arrange
    user_name_fields = {"first_name": "first", "last_name": "last"}
    user_data = {"username": "username", "email": "user@email.com", "password": "password"}
    user = AppUser.objects.create_user(**user_data)
    client.force_login(user)

    # Act
    response = client.post(reverse("account-details"), user_name_fields)
    result = response.context["result"]
    templates = [template.name for template in response.templates]
    user.refresh_from_db()

    # Assert
    assert user.first_name == user_name_fields["first_name"]
    assert user.last_name == user_name_fields["last_name"]
    assert "account/account-details.html" in templates
    assert result == "success"
