import pytest
from django.urls import reverse

from authentication.forms import SignInForm
from authentication.models import AppUser


@pytest.mark.django_db
def test_sign_in_view_get_method_authenticated_session(client):
    """
    GIVEN an authenticated session
    WHEN a GET request is made to the sign in view
    THEN redirect to the account details page
    """

    # Arrange
    user_data = {"username": "username", "email": "user@email.com", "password": "password"}
    user = AppUser.objects.create_user(**user_data)
    client.force_login(user)

    # Act
    response = client.get(reverse("sign-in"))

    # Assert
    assert response.status_code == 302
    assert response.url == reverse("account-details")


def test_sign_in_view_get_method_unauthenticated_session(client):
    """
    GIVEN an unauthenticated session
    WHEN a GET request is made to the sign in view
    THEN render the sign in page
    """

    # Act
    response = client.get(reverse("sign-in"))
    rendered_templates = [template.name for template in response.templates]

    # Assert
    assert "authentication/sign-in.html" in rendered_templates


@pytest.mark.parametrize(
    "email, password, expected_errors",
    [
        ("", "", {"email": ["This field is required."], "password": ["This field is required."]}),
        ("invalid_email", "valid_password", {"email": ["Enter a valid email address."]}),
    ],
)
def test_sign_in_view_post_method_invalid_data(client, email, password, expected_errors):
    """
    GIVEN sign in invalid data
    WHEN a POST request is made to the sign in view
    THEN render the sign in page with the form errors
    """

    # Arrange
    user_credentials = {"email": email, "password": password}

    # Act
    response = client.post(reverse("sign-in"), user_credentials)
    sign_in_form: SignInForm = response.context["form"]
    rendered_templates = [template.name for template in response.templates]

    # Assert
    assert not sign_in_form.is_valid()
    assert all(sign_in_form.errors[field] == error for field, error in expected_errors.items())
    assert "authentication/sign-in.html" in rendered_templates


@pytest.mark.django_db
def test_sign_in_view_post_method_invalid_credentials(client):
    """
    GIVEN sign in invalid credentials
    WHEN a POST request is made to the sign in view
    THEN render the sign in page with the form errors
    """

    # Arrange
    user_credentials = {"email": "user@email.com", "password": "password"}

    # Act
    response = client.post(reverse("sign-in"), user_credentials)
    sign_in_form: SignInForm = response.context["form"]
    rendered_templates = [template.name for template in response.templates]

    # Assert
    assert not sign_in_form.is_valid()
    assert sign_in_form.non_field_errors() == ["Invalid email or password"]
    assert "authentication/sign-in.html" in rendered_templates


@pytest.mark.django_db
def test_sign_in_view_post_method_valid_data(client):
    """
    GIVEN sign in valid data
    WHEN a POST request is made to the sign in view
    THEN redirect to the account page with the user authenticated
    """

    # Arrange
    user_credentials = {"email": "user@email.com", "password": "password"}
    user_data = {"username": "username"} | user_credentials
    user = AppUser.objects.create_user(**user_data)

    # Act
    response = client.post(reverse("sign-in"), user_credentials)

    # Assert
    assert response.url == reverse("account-details")
    assert response.client.session["_auth_user_id"] == str(user.id)
