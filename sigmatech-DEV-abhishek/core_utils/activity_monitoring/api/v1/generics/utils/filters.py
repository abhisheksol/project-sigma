import django_filters

from core_utils.activity_monitoring.models import (
    ActivityMonitoringLogModel,
)
from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.filter_utils import (
    ChoiceInFilter,
    DateRangeCommaSeparatedFilter,
    UUIDInFilter,
)


class ActivityMonitoringLogFilterSet(django_filters.FilterSet):
    core_generic_created_at = DateRangeCommaSeparatedFilter(
        field_name="core_generic_created_at"
    )

    activity_type = UUIDInFilter(
        field_name="activity_type__id",
        lookup_expr="in",
    )
    performed_by = UUIDInFilter(
        field_name="performed_by__id",
        lookup_expr="in",
    )
    method = ChoiceInFilter(
        field_name="method",
        choices=ActivityMonitoringMethodTypeEnumChoices.choices(),
        lookup_expr="in",
    )
    linked_entity = UUIDInFilter(
        field_name="activity_type__linked_entity__id",
        lookup_expr="in",
    )

    class Meta:
        model = ActivityMonitoringLogModel
        fields = [
            "core_generic_created_at",
            "activity_type",
            "method",
            "linked_entity",
            "performed_by",
        ]
