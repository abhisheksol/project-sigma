from django.core.management.base import BaseCommand
from store.configurations.loan_config.template_config.enums import (
    DateFormatEnum,
    DateTimeFormatEnum,
    DurationFormatEnum,
)
from store.configurations.loan_config.template_config.models import SQLDataTypeModel
from typing import Dict


class Command(BaseCommand):

    def handle(self, *args, **options):
        rules: Dict[str, Dict[str, str]] = {
            "string": {},
            "integer": {},
            "decimal": {},
            "float": {},
            "boolean": {},
            "date": {
                "date_format": DateFormatEnum.ISO_DATE.value,
            },
            "datetime": {
                "datetime_format": DateTimeFormatEnum.ISO_DATETIME.value,
            },
            "time": {
                "duration_format": DurationFormatEnum.HOURS_MINUTES_SECONDS.value,
            },
        }

        for title, config in rules.items():
            obj, created = SQLDataTypeModel.objects.get_or_create(title=title)
            for field, value in config.items():
                setattr(obj, field, value)
            obj.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created {title} SQL data type"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated {title} SQL data type"))

        self.stdout.write(self.style.SUCCESS("✅ SQL data types seeded successfully"))
