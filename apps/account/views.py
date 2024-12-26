from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from apps.account.forms import AccountDetailsForm


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

    def post(self, request: WSGIRequest) -> HttpResponse:
        """
        Handles the account details form submission.

        Parameters
        ----------
        request : WSGIRequest
            The request object.

        Returns
        -------
        HttpResponse
            The account details page with the form if the form is invalid,
            otherwise the account details page with the result as success.
        """

        account_details_form = AccountDetailsForm(request.POST, instance=request.user)

        if not account_details_form.is_valid():
            return render(
                request,
                "authentication/sign-in.html",
                {"form": account_details_form},
            )

        account_details_form.save()

        return render(request, "account/account-details.html", {"result": "success"})
