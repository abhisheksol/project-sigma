from django_filters import rest_framework as filters
from typing import List
from core_utils.notifications.models import NotificationModel


class NotificationModelFilterSet(filters.FilterSet):
    is_mention = filters.BooleanFilter(field_name="is_mention")
    is_cleared = filters.BooleanFilter(field_name="is_cleared")
    proposal_id = filters.BaseInFilter(field_name="proposal_id__pk")
    mentioned_by = filters.BaseInFilter(field_name="mentioned_by__pk")
    time_period = filters.DateFromToRangeFilter(field_name="core_generic_created_at")

    class Meta:
        model: NotificationModel = NotificationModel
        fields: List[str] = ["is_mention", "is_cleared", "proposal_id", "mentioned_by"]
