import django_filters
from store.operations.allocation_files.models import AllocationFileModel


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    """Custom filter to handle multiple string values separated by commas"""


class AllocationFileFilter(django_filters.FilterSet):

    process_ids = django_filters.BaseInFilter(
        field_name="product_assignment__process__id", lookup_expr="in"
    )
    product_ids = django_filters.BaseInFilter(
        field_name="product_assignment__product__id", lookup_expr="in"
    )

    # Allocation status multi-select
    status = CharInFilter(field_name="allocation_status", lookup_expr="in")

    upload_date = django_filters.CharFilter(method="filter_upload_date")

    def filter_upload_date(self, queryset, name, value):
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

    class Meta:
        model = AllocationFileModel
        fields = []
