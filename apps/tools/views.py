from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from apps.tools.tool_factory.factory import ToolFactory
from apps.tools.tool_factory.tools.background_remover import BackgroundRemover


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
            background_remover = ToolFactory[BackgroundRemover].create_tool("background_remover")
            background_remover.load_image_model()

            img_bytes, img_format, img_name = background_remover.process(img_file=img_file)

            response = HttpResponse(img_bytes, content_type=f"image/{img_format}")
            response["Content-Disposition"] = f'attachment; filename="{img_name}"'

            return response
        except Exception:
            return render(request, "tools/remove-background.html", {"error": "An error ocurred."})
