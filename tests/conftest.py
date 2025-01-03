import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

from aesthetiq.settings import BASE_DIR


@pytest.fixture(name="client")
def client_fixture() -> Client:
    """
    Client fixture.

    Returns
    -------
    Client
        The client instance.
    """

    return Client()


@pytest.fixture(name="image")
def image_fixture() -> SimpleUploadedFile:
    """
    Image fixture.

    Returns
    -------
    SimpleUploadedFile
        The image file.
    """

    image_path = os.path.join(BASE_DIR, "tests", "test_image.jpg")

    with open(image_path, "rb") as image_file:
        return SimpleUploadedFile(
            name="image.jpg", content=image_file.read(), content_type="image/jpeg"
        )
