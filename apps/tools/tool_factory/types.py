from typing import NamedTuple


class GeneratedImage(NamedTuple):
    """
    Generated image type.
    """

    img_bytes: bytes
    img_format: str
    img_name: str
