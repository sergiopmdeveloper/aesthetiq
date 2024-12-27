from django.contrib.auth.models import AbstractUser
from django.db import models

from authentication.validators import NAME_VALIDATOR


class AppUser(AbstractUser):
    """
    App user model.
    """

    email = models.EmailField(unique=True, error_messages={"unique": "Email already exists."})
    email_confirmed = models.BooleanField(default=False)

    first_name = models.CharField(
        max_length=150,
        blank=True,
        validators=[NAME_VALIDATOR],
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        validators=[NAME_VALIDATOR],
    )

    def __str__(self) -> str:
        """
        String representation of the user.

        Returns
        -------
        str
            The email of the user.
        """

        return self.email

    class Meta:
        """
        Metadata options.
        """

        db_table = "users"
        verbose_name_plural = "Users"
