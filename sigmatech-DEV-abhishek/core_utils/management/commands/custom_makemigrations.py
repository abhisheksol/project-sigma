from django.core.management import call_command
from django.core.management.base import BaseCommand

from django.conf import settings
from core_utils.utils.db_utils.get_custom_apps import GetCustomApps
from django.conf import settings
from typing import List

CUSTOM_APPS: List = getattr(settings, "CUSTOM_APPS", [])


class Command(BaseCommand, GetCustomApps):
    """
    Custom Django management command to run `makemigrations` for multiple apps in the project.
    """

    help = "Runs makemigrations for multiple apps in the project"

    def handle(self, *args, **kwargs):
        """
        Executes the command to run `makemigrations` on all custom apps.

        This method processes the list of custom apps, extracts the relevant app names,
        and then calls the `makemigrations` command for them.
        """
        custom_apps: list = self.refactor_command(CUSTOM_APPS)
        self.stdout.write(f"Running makemigrations for apps: {custom_apps}")

        try:
            # ? Run makemigrations for the extracted app names
            call_command("makemigrations", *custom_apps)
            self.stdout.write(
                f"Successfully ran makemigrations for apps: {custom_apps}"
            )
        except Exception as e:
            self.stderr.write(
                f"Error running makemigrations for apps {custom_apps}: {e}"
            )
