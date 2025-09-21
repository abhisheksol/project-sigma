import os
from typing import List

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command


class Command(BaseCommand):
    """
    Django custom management command to load all `.json` fixture files
    from a predefined directory using `loaddata`.
    """

    help: str = "Loads all fixture files from the given directory using loaddata"

    def add_arguments(self, parser) -> None:
        """
        No additional arguments for this command.
        Directory is hardcoded as 'project_utils/loaddata'.
        """

    def handle(self, *args, **options) -> None:
        """
        Entry point for the management command.
        Loads all `.json` fixtures found in the specified directory.
        """

        # Directory path where fixture files are stored
        directory: str = "project_utils/loaddata"

        # Validate that the directory exists
        if not os.path.isdir(directory):
            raise CommandError(f"'{directory}' is not a valid directory")

        # Supported fixture file extensions
        valid_extensions: List[str] = [".json"]

        # List all valid fixture files in the directory
        fixture_files: List[str] = [
            f
            for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
            and os.path.splitext(f)[1] in valid_extensions
        ]

        # If no fixtures are found, print a warning and exit
        if not fixture_files:
            self.stdout.write(
                self.style.WARNING("No fixture files found in the directory.")
            )
            return

        # Load each fixture file using the `loaddata` command
        for fixture_file in fixture_files:
            fixture_path: str = os.path.join(directory, fixture_file)
            self.stdout.write(f"Loading fixture: {fixture_file}")

            try:
                print("fixture_path.lower()", fixture_path.lower())
                if "RegionAppPublicData.json".lower() not in fixture_path.lower():
                    call_command("loaddata", fixture_path)
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfully loaded {fixture_file}")
                    )
                else:
                    self.stdout.write(self.style.SUCCESS(f"{fixture_file} skipped"))
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(f"Failed to load {fixture_file}: {e}")
                )
