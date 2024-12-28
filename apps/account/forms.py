from django.forms import ModelForm

from authentication.models import AppUser


class AccountDetailsForm(ModelForm):
    """
    Account details form.
    """

    class Meta:
        """
        Metadata options.
        """

        model = AppUser
        fields = ["first_name", "last_name"]
