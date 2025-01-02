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
