from django.contrib.auth import login, logout
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
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
            return redirect(reverse("account-details"))

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
            The sign in page with the form if the form is invalid,
            otherwise the redirection to the account details page.
        """

        sign_in_form = SignInForm(request.POST)

        if not sign_in_form.is_valid():
            return render(
                request,
                "authentication/sign-in.html",
                {"form": sign_in_form},
            )

        login(request, sign_in_form.user)

        return redirect(reverse("account-details"))


class SignOutView(View):
    """
    Sign out view.
    """

    def post(self, request: WSGIRequest) -> HttpResponseRedirect:
        """
        Signs out the user.

        Parameters
        ----------
        request : WSGIRequest
            The request object.

        Returns
        -------
        HttpResponseRedirect
            The redirection to the sign in page.
        """

        logout(request)

        return redirect(reverse("sign-in"))
