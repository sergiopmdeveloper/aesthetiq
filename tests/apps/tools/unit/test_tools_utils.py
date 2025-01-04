import base64

from apps.tools.utils import convert_image_to_base64


def test_convert_image_to_base64_ok():
    """
    GIVEN image bytes and content type
    WHEN convert_image_to_base64 function is called
    THEN return the base64 data URL of the image
    """

    # Arrange
    img_bytes = b"image"
    content_type = "image/png"
    expected_data_url = f"data:{content_type};base64,{base64.b64encode(img_bytes).decode("utf-8")}"

    # Act
    result = convert_image_to_base64(img_bytes, content_type)

    # Assert
    assert result == expected_data_url
