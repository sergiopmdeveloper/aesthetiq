from unittest.mock import patch

import pytest
from django.urls import reverse

from authentication.models import AppUser


@pytest.mark.django_db
def test_remove_background_view_get_method_authenticated_session(client):
    """
    GIVEN an authenticated session
    WHEN a GET request is made to the remove background view
    THEN render the remove background page
    """

    # Arrange
    user_data = {"username": "username", "email": "user@email.com", "password": "password"}
    user = AppUser.objects.create_user(**user_data)
    client.force_login(user)

    # Act
    response = client.get(reverse("remove-background"))
    templates = [template.name for template in response.templates]

    # Assert
    assert "tools/remove-background.html" in templates


def test_remove_background_view_get_method_unauthenticated_session(client):
    """
    GIVEN an unauthenticated session
    WHEN a GET request is made to the remove background view
    THEN redirect to the sign in page
    """

    # Act
    response = client.get(reverse("remove-background"))

    # Assert
    assert response.status_code == 302
    assert response.url == reverse("sign-in") + f"?next={reverse('remove-background')}"


def test_remove_background_view_post_method_no_image_given(client):
    """
    GIVEN no image
    WHEN a POST request is made to the remove background view
    THEN render the remove background page with an error message
    """

    # Act
    response = client.post(reverse("remove-background"))
    error = response.context["error"]

    # Assert
    assert error == "No image provided."


def test_remove_background_view_post_method_image_given(client, image, background_remover_mock):
    """
    GIVEN an image
    WHEN a POST request is made to the remove background view
    THEN render the remove background page with the original and processed images
    """

    # Arrange
    data = {"image": image}

    # Act
    with patch(
        "apps.tools.views.ToolFactory.create_service",
        return_value=background_remover_mock,
    ):
        response = client.post(reverse("remove-background"), data)
        original_data_url = response.context.get("original_image")
        processed_data_url = response.context.get("processed_image")
        templates = [template.name for template in response.templates]

    # Assert
    assert original_data_url is not None
    assert processed_data_url is not None
    assert "tools/remove-background.html" in templates


def test_remove_background_view_post_method_exception(client, image, background_remover_mock):
    """
    GIVEN an image
    WHEN a POST request is made to the remove background view and an exception is raised
    THEN render the remove background page with an error message
    """

    # Arrange
    background_remover_mock.process.side_effect = Exception("Error")
    data = {"image": image}

    # Act
    with patch(
        "apps.tools.views.ToolFactory.create_service",
        return_value=background_remover_mock,
    ):
        response = client.post(reverse("remove-background"), data)
        error = response.context.get("error")
        templates = [template.name for template in response.templates]

    # Assert
    assert error == "An error occurred."
    assert "tools/remove-background.html" in templates
