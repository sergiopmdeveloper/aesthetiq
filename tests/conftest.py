import pytest
from django.test import Client


@pytest.fixture(name="client")
def client_fixture() -> Client:
    """
    Client fixture.

    Returns
    -------
    Client
        The client instance.
    """

    return Client()
