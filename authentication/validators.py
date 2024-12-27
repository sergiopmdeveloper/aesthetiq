from django.core.validators import RegexValidator

NAME_VALIDATOR = RegexValidator(
    regex=r"^[a-zA-Z\s]*$", message="Only letters and spaces are allowed."
)
