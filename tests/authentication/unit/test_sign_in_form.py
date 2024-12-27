import pytest

from authentication.forms import SignInForm
from authentication.models import AppUser


@pytest.mark.parametrize(
    "email, password, expected_errors",
    [
        ("", "", {"email": ["This field is required."], "password": ["This field is required."]}),
        ("invalid_email", "valid_password", {"email": ["Enter a valid email address."]}),
    ],
)
def test_sign_in_form_invalid_data(email, password, expected_errors):
    """
    GIVEN a sign in form with invalid data
    WHEN the form is validated
    THEN check if the form errors match the expected errors
    """

    # Arrange
    user_credentials = {"email": email, "password": password}

    # Act
    form = SignInForm(user_credentials)

    # Assert
    assert not form.is_valid()
    assert all(form.errors[field] == error for field, error in expected_errors.items())


@pytest.mark.django_db
def test_sign_in_form_invalid_credentials():
    """
    GIVEN a sign in form with invalid credentials
    WHEN the form is validated
    THEN check if the form errors match the expected errors
    """

    # Arrange
    user_credentials = {"email": "user@email.com", "password": "password"}

    # Act
    form = SignInForm(user_credentials)

    # Assert
    assert not form.is_valid()
    assert form.non_field_errors() == ["Invalid email or password"]


@pytest.mark.django_db
def test_sign_in_form_valid_data():
    """
    GIVEN a sign in form with valid data
    WHEN the form is validated
    THEN check if the form is valid
    """

    # Arrange
    user_credentials = {"email": "user@email.com", "password": "password"}
    user_data = {"username": "username"} | user_credentials
    AppUser.objects.create_user(**user_data)

    # Act
    form = SignInForm(user_credentials)

    # Assert
    assert form.is_valid()
