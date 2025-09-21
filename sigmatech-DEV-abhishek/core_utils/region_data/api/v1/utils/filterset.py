import django_filters
from core_utils.region_data.models import StateModel, CityModel
from typing import List


class StateFilterSet(django_filters.FilterSet):

    class Meta:
        model: StateModel = StateModel
        fields: List = ["country"]


class CityFilterSet(django_filters.FilterSet):

    class Meta:
        model: CityModel = CityModel
        fields: List = ["state", "country"]
