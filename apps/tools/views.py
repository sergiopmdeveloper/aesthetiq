import io

from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from PIL import Image
from rembg import remove


class RemoveBackgroundView(View):
    """
    Remove background view.
    """

    @method_decorator(login_required)
    def get(self, request: WSGIRequest) -> HttpResponse:
        """
        Renders the remove background page.

        Parameters
        ----------
        request : WSGIRequest
            The request object.

        Returns
        -------
        HttpResponse
            The remove background page.
        """

        return render(request, "tools/remove-background.html")

    def post(self, request: WSGIRequest) -> HttpResponse:
        """
        Handles the remove background request.

        Parameters
        ----------
        request : WSGIRequest
            The request object.

        Returns
        -------
        HttpResponse
            ...
        """

        input_image_file = request.FILES.get("image")

        if not input_image_file:
            return render(request, "tools/remove-background.html", {"error": "No image provided."})

        try:
            input_img = Image.open(input_image_file)

            input_img_buffer = io.BytesIO()
            input_img.save(input_img_buffer, format=input_img.format)
            input_img_bytes = input_img_buffer.getvalue()

            output_img_bytes = remove(input_img_bytes)
            output_img_format = input_img.format.lower()
            output_img_name = input_image_file.name + "_no_bg" + output_img_format

            response = HttpResponse(output_img_bytes, content_type=f"image/{output_img_format}")
            response["Content-Disposition"] = f'attachment; filename="{output_img_name}"'

            return response
        except Exception:
            return render(request, "tools/remove-background.html", {"error": "An error ocurred."})
