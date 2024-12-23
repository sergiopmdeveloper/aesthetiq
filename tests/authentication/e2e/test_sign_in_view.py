import pytest

from authentication.forms import SignInForm
from authentication.models import AppUser
from tests.constants import USER_DATA


@pytest.mark.django_db
def test_sign_in_view_get_method_authenticated(client):
    """
    GIVEN an authenticated session
    WHEN a GET request is made to the sign in view
    THEN redirect to the account page
    """

    # Arrange
    user = AppUser.objects.create_user(**USER_DATA)
    client.force_login(user)

    # Act
    response = client.get("/authentication/sign-in")

    # Assert
    assert response.url == "/account"


def test_sign_in_view_get_method_not_authenticated(client):
    """
    GIVEN an unauthenticated session
    WHEN a GET request is made to the sign in view
    THEN render the sign in page
    """

    # Act
    response = client.get("/authentication/sign-in")
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
def test_sign_in_view_post_method_invalid_form(client, email, password, expected_errors):
    """
    GIVEN a sign in form with invalid data
    WHEN a POST request is made to the sign in view
    THEN render the sign in page with the form errors
    """

    # Act
    response = client.post("/authentication/sign-in", data={"email": email, "password": password})
    sign_in_form: SignInForm = response.context["form"]
    rendered_templates = [template.name for template in response.templates]

    # Assert
    assert not sign_in_form.is_valid()
    for field, error in expected_errors.items():
        assert sign_in_form.errors[field] == error
    assert "authentication/sign-in.html" in rendered_templates


@pytest.mark.django_db
def test_sign_in_view_post_method_invalid_credentials(client):
    """
    GIVEN a sign in form with invalid credentials
    WHEN a POST request is made to the sign in view
    THEN render the sign in page with the form errors
    """

    # Act
    response = client.post(
        "/authentication/sign-in", data={"email": "user@email.com", "password": "password"}
    )
    sign_in_form: SignInForm = response.context["form"]
    rendered_templates = [template.name for template in response.templates]

    # Assert
    assert not sign_in_form.is_valid()
    assert sign_in_form.non_field_errors() == ["Invalid email or password"]
    assert "authentication/sign-in.html" in rendered_templates


@pytest.mark.django_db
def test_sign_in_view_post_method_valid_form(client):
    """
    GIVEN a sign in form with valid data
    WHEN a POST request is made to the sign in view
    THEN redirect to the account page with the user authenticated
    """

    # Arrange
    user = AppUser.objects.create_user(**USER_DATA)

    # Act
    response = client.post(
        "/authentication/sign-in",
        data={"email": USER_DATA["email"], "password": USER_DATA["password"]},
    )

    # Assert
    assert response.url == "/account"
    assert response.client.session["_auth_user_id"] == str(user.id)
