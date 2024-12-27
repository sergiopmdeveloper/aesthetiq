import os
import sys

from aesthetiq.constants import DJANGO_NOT_INSTALLED_MSG
from aesthetiq.utils import verifyEnvVariables


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aesthetiq.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as e:
        raise ImportError(DJANGO_NOT_INSTALLED_MSG) from e

    verifyEnvVariables()

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
