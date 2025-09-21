import django_filters
from django.utils import timezone
from store.operations.allocation_files.models import AllocationFileModel
from django.db import models


class AllocationFileFilter(django_filters.FilterSet):
    # Multiple IDs
    process_ids = django_filters.BaseInFilter(
        field_name="product_assignment__process__id", lookup_expr="in"
    )
    product_ids = django_filters.BaseInFilter(
        field_name="product_assignment__product__id", lookup_expr="in"
    )

    # Date range
    upload_date_from = django_filters.DateTimeFilter(
        field_name="core_generic_created_at", lookup_expr="gte"
    )
    upload_date_to = django_filters.DateTimeFilter(
        field_name="core_generic_created_at", lookup_expr="lte"
    )

    # Status (custom method filter)
    status = django_filters.CharFilter(method="filter_status")

    class Meta:
        model = AllocationFileModel
        fields = []

    def filter_status(self, queryset, name, value):
        now = timezone.now()
        if value.upper() == "ERROR":
            return queryset.filter(no_of_error_records__gt=0)
        elif value.upper() == "EXPIRED":
            return queryset.filter(expiry_date__lt=now)
        elif value.upper() == "VALID":
            return queryset.filter(no_of_error_records=0).filter(
                models.Q(expiry_date__gte=now) | models.Q(expiry_date__isnull=True)
            )
        return queryset
