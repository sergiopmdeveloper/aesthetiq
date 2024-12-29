from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View


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

    def post(self, _: WSGIRequest) -> HttpResponse:
        """
        Handles the remove background request.

        Parameters
        ----------
        _ : WSGIRequest
            The request object, not used for now.

        Returns
        -------
        HttpResponse
            ...
        """

        return HttpResponse("Not implemented yet...")
