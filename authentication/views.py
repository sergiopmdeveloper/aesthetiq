from django.contrib.auth import login
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from authentication.forms import SignInForm


class SignInView(View):
    """
    Sign in view.
    """

    @method_decorator(never_cache)
    def get(self, request: WSGIRequest) -> HttpResponse:
        """
        Renders the sign in page.

        Parameters
        ----------
        request : WSGIRequest
            The request object.

        Returns
        -------
        HttpResponse
            The sign in page.
        """

        if request.user.is_authenticated:
            return redirect("/account")

        return render(request, "authentication/sign-in.html")

    def post(self, request: WSGIRequest) -> HttpResponse | HttpResponseRedirect:
        """
        Handles the sign in form submission.

        Parameters
        ----------
        request : WSGIRequest
            The request object.

        Returns
        -------
        HttpResponse | HttpResponseRedirect
            The sign in page if the form is invalid,
            otherwise the account page.
        """

        sign_in_form = SignInForm(request.POST)

        if not sign_in_form.is_valid():
            return render(
                request,
                "authentication/sign-in.html",
                {"form": sign_in_form},
            )

        login(request, sign_in_form.user)

        return redirect("/account")
