from aesthetiq import settings
from aesthetiq.errors import EnvError


def verifyEnvVariables():
    """
    Verifies the presence of required environment variables.
    """

    if not settings.SECRET_KEY:
        raise EnvError("SECRET_KEY is not set")

    if not settings.ENVIRONMENT:
        raise EnvError("ENVIRONMENT is not set")
