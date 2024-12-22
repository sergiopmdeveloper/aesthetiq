from django.forms import EmailField, ModelForm, ValidationError

from authentication.models import AppUser


class SignInForm(ModelForm):
    """
    Sign in form.

    Attributes
    ----------
    email : EmailField
        The overridden email field.
    user : Optional[AppUser]
        The user if the credentials are valid.

    Methods
    -------
    clean()
        Custom form validation.
    _validate_user_credentials(email, password)
        Validates the user credentials.
    """

    email = EmailField()
    user = None

    def clean(self) -> None:
        """
        Custom form validation.
        """

        data = super().clean()

        if not self.errors.get("email") and not self.errors.get("password"):
            self._validate_user_credentials(data["email"], data["password"])

    def _validate_user_credentials(self, email: str, password: str) -> None:
        """
        Validates the user credentials.

        Parameters
        ----------
        email : str
            The email of the user.
        password : str
            The password of the user.

        Raises
        ------
        ValidationError
            If the user credentials are invalid.
        """

        user = AppUser.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            raise ValidationError("Invalid email or password")

        self.user = user

    class Meta:
        """
        Metadata options.
        """

        model = AppUser
        fields = ["password"]
