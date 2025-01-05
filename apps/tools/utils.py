import base64


def convert_image_to_base64(img_bytes: bytes, content_type: str) -> str:
    """
    Converts image bytes to a base64 data URL.

    Parameters
    ----------
    img_bytes : bytes
        The image bytes.
    content_type : str
        The content type of the image.

    Returns
    -------
    str
        The base64 data URL of the image.
    """

    base64_encoded = base64.b64encode(img_bytes).decode("utf-8")

    return f"data:{content_type};base64,{base64_encoded}"


def convert_base64_to_image(base64_str: str) -> bytes:
    """
    Converts a base64 data URL to image bytes.

    Parameters
    ----------
    base64_str : str
        The base64 data URL of the image.

    Returns
    -------
    bytes
        The image bytes.
    """

    base64_data = base64_str.split(",")[1]
    img_bytes = base64.b64decode(base64_data)

    return img_bytes
