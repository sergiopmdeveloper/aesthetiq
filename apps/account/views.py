from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View


class AccountDetailsView(View):
    """
    Account details view.
    """

    @method_decorator(login_required(login_url="/authentication/sign-in"))
    def get(self, request: WSGIRequest) -> HttpResponse:
        """
        Renders the account details page.

        Parameters
        ----------
        request : WSGIRequest
            The request object.

        Returns
        -------
        HttpResponse
            The account details page.
        """

        return render(request, "account/account-details.html")
