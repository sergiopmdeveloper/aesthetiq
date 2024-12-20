import os
import sys

import aesthetiq.settings as settings
from aesthetiq.constants import DJANGO_NOT_INSTALLED_MSG
from aesthetiq.errors import EnvError


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aesthetiq.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as e:
        raise ImportError(DJANGO_NOT_INSTALLED_MSG) from e

    if not settings.SECRET_KEY:
        raise EnvError("SECRET_KEY is not set")

    if not settings.ENVIRONMENT:
        raise EnvError("ENVIRONMENT is not set")

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
