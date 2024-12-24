import pytest

from authentication.forms import SignInForm


@pytest.mark.parametrize(
    "email, password, expected_errors",
    [
        ("", "", {"email": ["This field is required."], "password": ["This field is required."]}),
        ("invalid_email", "valid_password", {"email": ["Enter a valid email address."]}),
    ],
)
def test_sign_in_form_field_errors(email, password, expected_errors):
    """
    GIVEN a sign in form with invalid data
    WHEN the form is validated
    THEN check if the form errors match the expected errors
    """

    # Act
    form = SignInForm(data={"email": email, "password": password})

    # Assert
    assert not form.is_valid()
    for field, error in expected_errors.items():
        assert form.errors[field] == error


@pytest.mark.django_db
def test_sign_in_form_invalid_credentials():
    """
    GIVEN a sign in form with invalid credentials
    WHEN the form is validated
    THEN check if the form errors match the expected errors
    """

    # Act
    form = SignInForm(data={"email": "user@email.com", "password": "password"})

    # Assert
    assert not form.is_valid()
    assert form.non_field_errors() == ["Invalid email or password"]
