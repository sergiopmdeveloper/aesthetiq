from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from apps.tools.factories.tool_factory import ToolFactory
from apps.tools.forms import BackgroundRemoverResultForm
from apps.tools.models import BackgroundRemoverResult
from apps.tools.services.tool.modules.bg_remover import BackgroundRemover
from apps.tools.utils import convert_base64_to_image, convert_image_to_base64


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
            otherwise the remove background page with the original and processed images.
        """

        img_file = request.FILES.get("image")

        if not img_file:
            return render(request, "tools/remove-background.html", {"error": "No image provided."})

        try:
            original_bytes = img_file.read()

            original_data_url = convert_image_to_base64(
                img_bytes=original_bytes, content_type=img_file.content_type
            )

            background_remover = ToolFactory[BackgroundRemover].create_service("background_remover")
            background_remover.load_image_model()

            processed_bytes = background_remover.process(img_file=img_file)

            processed_data_url = convert_image_to_base64(
                img_bytes=processed_bytes, content_type=img_file.content_type
            )

            return render(
                request,
                "tools/remove-background.html",
                {"original_image": original_data_url, "processed_image": processed_data_url},
            )
        except Exception:
            return render(request, "tools/remove-background.html", {"error": "An error occurred."})


class SaveRemoveBackgroundResultView(View):
    """
    Save remove background result view.
    """

    def post(self, request: WSGIRequest) -> HttpResponse:
        """
        Handles the save remove background result request.

        Parameters
        ----------
        request : WSGIRequest
            The request object.

        Returns
        -------
        HttpResponse
            The remove background page with the error message if an error occurred,
            otherwise the remove background page with the result as success.
        """

        result_name = request.POST.get("result_name")
        original_image = request.POST.get("original_image")
        processed_image = request.POST.get("processed_image")

        background_remover_result_form = BackgroundRemoverResultForm(
            {
                "user": request.user,
                "result_name": result_name,
            }
        )

        if not background_remover_result_form.is_valid():
            return render(
                request,
                "tools/remove-background.html",
                {
                    "form": background_remover_result_form,
                    "original_image": original_image,
                    "processed_image": processed_image,
                },
            )

        BackgroundRemoverResult.objects.create(
            user=request.user,
            result_name=result_name,
            original_image=convert_base64_to_image(base64_str=original_image),
            processed_image=convert_base64_to_image(base64_str=processed_image),
        )

        return render(request, "tools/remove-background.html", {"result": "success"})
