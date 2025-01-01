import base64

from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from apps.tools.factories.tool_factory import ToolFactory
from apps.tools.services.tool.modules.bg_remover import BackgroundRemover


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
            The remove background page with the error message if an error occurred,
            otherwise the image with the background removed.
        """

        img_file = request.FILES.get("image")

        if not img_file:
            return render(request, "tools/remove-background.html", {"error": "No image provided."})

        try:
            original_bytes = img_file.read()
            original_base64 = base64.b64encode(original_bytes).decode("utf-8")
            original_format = img_file.content_type.split("/")[-1]
            original_data_url = f"data:image/{original_format};base64,{original_base64}"

            background_remover = ToolFactory[BackgroundRemover].create_service("background_remover")
            background_remover.load_image_model()
            processed_bytes, processed_format, _ = background_remover.process(img_file=img_file)

            processed_base64 = base64.b64encode(processed_bytes).decode("utf-8")
            processed_data_url = f"data:image/{processed_format};base64,{processed_base64}"

            return render(
                request,
                "tools/remove-background.html",
                {"original_image": original_data_url, "processed_image": processed_data_url},
            )
        except Exception:
            return render(request, "tools/remove-background.html", {"error": "An error ocurred."})
