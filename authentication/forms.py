from django.forms import ModelForm

from authentication.models import AppUser


class SignInForm(ModelForm):
    """
    Sign in form.
    """

    class Meta:
        """
        Metadata options.
        """

        model = AppUser
        fields = ["email", "password"]
