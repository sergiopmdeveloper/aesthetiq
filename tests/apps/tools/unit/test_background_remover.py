import os
from unittest.mock import mock_open, patch

import pytest
import requests

from apps.tools.services.tool.modules.bg_remover import BackgroundRemover


def test_background_remover_load_image_model_already_downloaded():
    """
    GIVEN the scenario where the model is already downloaded
    WHEN load_image_model method is called
    THEN do not download the model
    """

    # Arrange
    background_remover = BackgroundRemover()

    # Act
    with (
        patch("os.path.exists", return_value=True),
        patch("requests.get") as mock_requests_get,
    ):
        background_remover.load_image_model()

    # Assert
    mock_requests_get.assert_not_called()


def test_background_remover_load_image_model_not_downloaded():
    """
    GIVEN the scenario where the model is not downloaded
    WHEN load_image_model method is called
    THEN download the model and write to the file
    """

    # Arrange
    background_remover = BackgroundRemover()

    # Act
    with (
        patch("os.path.exists", return_value=False),
        patch("requests.get") as mock_requests_get,
        patch("builtins.open", new_callable=mock_open) as mock_file,
    ):
        background_remover.load_image_model()

    # Assert
    mock_requests_get.assert_called_once_with(background_remover.MODEL_URL, stream=True)
    mock_file.assert_called_once_with(os.path.expanduser(background_remover.MODEL_PATH), "wb")


def test_background_remover_load_image_model_failed_to_download():
    """
    GIVEN the scenario where the model download fails
    WHEN load_image_model method is called
    THEN raise a RequestException
    """

    # Arrange
    background_remover = BackgroundRemover()

    # Act
    with (
        patch("os.path.exists", return_value=False),
        patch("requests.get", side_effect=requests.RequestException("Error")),
    ):
        with pytest.raises(requests.RequestException) as e:
            background_remover.load_image_model()

    # Assert
    assert str(e.value) == "Failed to download the model: Error"


def test_background_remover_process_ok(image):
    """
    GIVEN an image file
    WHEN process method is called
    THEN return the bytes of the image with the background removed
    """

    # Arrange
    background_remover = BackgroundRemover()

    # Act
    with patch(
        "apps.tools.services.tool.modules.bg_remover.remove", return_value=b"image"
    ) as mock_remove:
        result = background_remover.process(img_file=image)

    # Assert
    mock_remove.assert_called_once()
    assert isinstance(result, bytes)


def test_background_remover_process_failed(image):
    """
    GIVEN an image file
    WHEN process method is called and remove method fails
    THEN raise an Exception
    """

    # Arrange
    background_remover = BackgroundRemover()

    # Act
    with patch(
        "apps.tools.services.tool.modules.bg_remover.remove", side_effect=Exception("Error")
    ):
        with pytest.raises(Exception) as e:
            background_remover.process(img_file=image)

    # Assert
    assert str(e.value) == "Failed to remove the background from the image: Error"
