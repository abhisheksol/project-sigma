import django_filters

from django.utils.dateparse import parse_date
import datetime


class DateRangeCommaSeparatedFilter(django_filters.Filter):
    """
    Accepts a single query param like:
    ?core_generic_created_at=2025-08-20,2025-08-22
    and applies a range filter between these two dates.
    """

    def filter(self, qs, value):
        if not value:
            return qs

        try:
            start_date_str, end_date_str = value.split(",", 1)
        except ValueError:
            # If only one date is given, just return that exact match
            start_date_str: datetime.date = value
            end_date_str: None = None

        start_date: datetime.date = parse_date(start_date_str.strip())
        end_date: datetime.date = (
            parse_date(end_date_str.strip()) if end_date_str else None
        )

        if start_date and end_date:
            return qs.filter(
                **{
                    f"{self.field_name}__date__range": (start_date, end_date),
                }
            )
        elif start_date:
            return qs.filter(**{f"{self.field_name}__date": start_date})
        return qs


# Generic "comma separated IN" filter for UUIDs
class UUIDInFilter(django_filters.BaseInFilter, django_filters.UUIDFilter):
    """Allows comma-separated UUIDs"""


# Generic "comma separated IN" filter for choices (like enums)
class ChoiceInFilter(django_filters.BaseInFilter, django_filters.ChoiceFilter):
    """Allows comma-separated values for choice fields"""


# Generic "comma separated IN" filter for dates
class DateInFilter(django_filters.BaseInFilter, django_filters.DateFilter):
    """Allows comma-separated values for dates"""
