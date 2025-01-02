import io
import os

import requests
from django.core.files.uploadedfile import UploadedFile
from PIL import Image
from rembg import remove

from apps.tools.services.tool.interfaces import Tool


class BackgroundRemover(Tool):
    """
    Background remover tool.

    Attributes
    ----------
    MODEL_URL : str
        The URL of the background remover model.
    MODEL_PATH : str
        The path of the background remover model.

    Methods
    -------
    load_image_model() -> None
        Loads the background remover model.
    process(img_file: UploadedFile) -> bytes
        Removes the background from an image.
    """

    MODEL_URL = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"
    MODEL_PATH = "~/.u2net/u2net.onnx"

    def load_image_model(self) -> None:
        """
        Loads the background remover model.
        """

        destination = os.path.expanduser(self.MODEL_PATH)
        os.makedirs(os.path.dirname(destination), exist_ok=True)

        if os.path.exists(destination):
            return

        try:
            response = requests.get(self.MODEL_URL, stream=True)
            response.raise_for_status()

            with open(destination, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        except requests.RequestException as e:
            e_msg = f"Failed to download the model: {e}"
            raise e(e_msg)

    def process(self, img_file: UploadedFile) -> bytes:
        """
        Removes the background from an image.

        Parameters
        ----------
        img_file : UploadedFile
            The image file.

        Returns
        -------
        bytes
            The bytes of the image with the background removed.
        """

        try:
            input_img = Image.open(img_file)

            input_img_buffer = io.BytesIO()
            input_img.save(input_img_buffer, format=input_img.format)
            input_img_bytes = input_img_buffer.getvalue()

            output_img_bytes = remove(input_img_bytes)

            return output_img_bytes
        except Exception as e:
            e_msg = f"Failed to remove the background from the image: {e}"
            raise Exception(e_msg)
