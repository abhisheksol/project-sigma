import os
import shutil

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help: str = "Deletes all migration folders and their contents from all Django apps"

    def handle(self, *args, **kwargs):
        # ? Get the project root directory
        project_root = os.getcwd()
        # ? Get all app directories
        for root, dirs, files in os.walk(project_root):
            if "migrations" in dirs:
                migrations_dir = os.path.join(root, "migrations")
                self.stdout.write(f"Deleting migrations folder: {migrations_dir}")

                # Remove the migrations directory and all its contents
                try:
                    shutil.rmtree(migrations_dir)
                    self.stdout.write(
                        f"Successfully removed directory: {migrations_dir}"
                    )
                except Exception as e:
                    self.stderr.write(f"Error removing directory {migrations_dir}: {e}")
