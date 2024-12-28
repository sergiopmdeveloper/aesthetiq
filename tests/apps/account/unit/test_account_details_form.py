import pytest

from apps.account.forms import AccountDetailsForm


@pytest.mark.parametrize(
    "first_name, last_name, expected_errors",
    [
        (
            "invalid_first_name",
            "invalid_last_name",
            {
                "first_name": ["Only letters and spaces are allowed."],
                "last_name": ["Only letters and spaces are allowed."],
            },
        ),
    ],
)
def test_account_details_form_invalid_data(first_name, last_name, expected_errors):
    """
    GIVEN account details invalid data
    WHEN the form is validated
    THEN check if the form errors match the expected errors
    """

    # Arrange
    user_name_fields = {"first_name": first_name, "last_name": last_name}

    # Act
    form = AccountDetailsForm(user_name_fields)

    # Assert
    assert not form.is_valid()
    assert all(form.errors[field] == error for field, error in expected_errors.items())


@pytest.mark.django_db
def test_account_details_form_valid_data():
    """
    GIVEN account details valid data
    WHEN the form is validated
    THEN check if the form is valid
    """

    # Arrange
    user_name_fields = {"first_name": "first", "last_name": "last"}

    # Act
    form = AccountDetailsForm(user_name_fields)

    # Assert
    assert form.is_valid()
