import django_filters
from store.operations.case_management.models import CaseManagementCaseModel


class CaseAllocationFilter(django_filters.FilterSet):
    # Existing filters
    min_mad = django_filters.NumberFilter(
        field_name="minimum_due_amount", lookup_expr="gte"
    )
    max_mad = django_filters.NumberFilter(
        field_name="minimum_due_amount", lookup_expr="lte"
    )
    min_dpd = django_filters.NumberFilter(field_name="current_dpd", lookup_expr="gte")
    max_dpd = django_filters.NumberFilter(field_name="current_dpd", lookup_expr="lte")

    region_ids = django_filters.BaseInFilter(  # region UUIDs
        field_name="residential_pin_code__city__zone__region__id", lookup_expr="in"
    )
    city_ids = django_filters.BaseInFilter(  # city   UUIDs
        field_name="residential_pin_code__city__id", lookup_expr="in"
    )
    zone_ids = django_filters.BaseInFilter(  # zone UUIDs
        field_name="residential_pin_code__city__zone__id", lookup_expr="in"
    )
    pincode_ids = django_filters.BaseInFilter(  # pincode UUIDs
        field_name="residential_pin_code__id", lookup_expr="in"
    )

    # field_mapping_status
    field_mapping_status = django_filters.CharFilter(
        field_name="field_mapping_status", lookup_expr="iexact"
    )

    # allocation_file id
    allocation_file_id = django_filters.BaseInFilter(
        field_name="allocation_file_id", lookup_expr="in"
    )

    # Batch metadata filters
    process_ids = django_filters.BaseInFilter(
        field_name="allocation_file__product_assignment__process_id", lookup_expr="in"
    )
    product_ids = django_filters.BaseInFilter(
        field_name="allocation_file__product_assignment__product_id", lookup_expr="in"
    )
    bucket_ids = django_filters.BaseInFilter(field_name="bucket_id", lookup_expr="in")
    cycle_ids = django_filters.BaseInFilter(
        field_name="allocation_file__cycle_id", lookup_expr="in"
    )

    # Date range (comma-separated: 2025-09-01,2025-09-04)
    upload_date = django_filters.CharFilter(method="filter_upload_date")

    def filter_upload_date(
        self, queryset: CaseManagementCaseModel, name: str, value: str
    ):
        try:
            dates = value.split(",")
            if len(dates) == 2:
                start, end = dates[0], dates[1]
                if start:
                    queryset = queryset.filter(core_generic_created_at__date__gte=start)
                if end:
                    queryset = queryset.filter(core_generic_created_at__date__lte=end)
        except Exception:
            pass
        return queryset

    unassigned: django_filters = django_filters.BooleanFilter(
        method="filter_unassigned"
    )

    risk: django_filters = django_filters.BaseInFilter(
        field_name="risk", lookup_expr="in"
    )

    def filter_unassigned(
        self, queryset: CaseManagementCaseModel, name: str, value: bool
    ):
        if value:  # if "Show Unassigned Cases" is toggled ON
            return queryset.filter(status__isnull=True)
        return queryset

    class Meta:
        model = CaseManagementCaseModel
        fields = ["status", "bucket"]
