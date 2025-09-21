from store.configurations.region_config.models import (
    RegionConfigurationAreaModel,
    RegionConfigurationPincodeModel,
)
import django_filters

from store.configurations.region_config.models import (
    RegionConfigurationCityModel,
)


# city filers ==>
# By City/Area name
# Select city/area name(s)

# By region
# Select region(s)

# By zone
# Select zone(s)

# By pin code
# Select pin codes

# By Sub-area
# Select sub-area name(s)


class RegionConfigurationCityFilter(django_filters.FilterSet):
    city_id = django_filters.BaseInFilter(field_name="id", lookup_expr="in")

    region_id = django_filters.BaseInFilter(
        field_name="zone__region__id", lookup_expr="in"
    )

    zone_id = django_filters.BaseInFilter(field_name="zone__id", lookup_expr="in")

    pincode_id = django_filters.BaseInFilter(
        field_name="RegionConfigurationPincodeModel_city__id", lookup_expr="in"
    )

    area_id = django_filters.BaseInFilter(
        field_name="RegionConfigurationPincodeModel_city__RegionConfigurationAreaModel_pincode__id",
        lookup_expr="in",
    )

    class Meta:
        model = RegionConfigurationCityModel
        fields = [
            "city_id",
            "region_id",
            "zone_id",
            "pincode_id",
            "area_id",
        ]


class RegionConfigurationPincodeFilter(django_filters.FilterSet):
    # filter by pincode id(s)
    pincode_id = django_filters.BaseInFilter(field_name="id", lookup_expr="in")

    # filter by region id(s)
    region_id = django_filters.BaseInFilter(
        field_name="city__zone__region__id", lookup_expr="in"
    )

    # filter by zone id(s)
    zone_id = django_filters.BaseInFilter(field_name="city__zone__id", lookup_expr="in")

    # filter by city id(s)
    city_id = django_filters.BaseInFilter(field_name="city__id", lookup_expr="in")

    # filter by area id(s)
    area_id = django_filters.BaseInFilter(
        field_name="RegionConfigurationAreaModel_pincode__id", lookup_expr="in"
    )

    class Meta:
        model = RegionConfigurationPincodeModel
        fields = [
            "pincode_id",
            "region_id",
            "zone_id",
            "city_id",
            "area_id",
        ]


class RegionConfigurationAreaFilter(django_filters.FilterSet):
    # direct area filter
    area_id = django_filters.BaseInFilter(field_name="id", lookup_expr="in")

    # by pincode
    pincode_id = django_filters.BaseInFilter(field_name="pincode__id", lookup_expr="in")

    # by city
    city_id = django_filters.BaseInFilter(
        field_name="pincode__city__id", lookup_expr="in"
    )

    # by zone
    zone_id = django_filters.BaseInFilter(
        field_name="pincode__city__zone__id", lookup_expr="in"
    )

    # by region
    region_id = django_filters.BaseInFilter(
        field_name="pincode__city__zone__region__id", lookup_expr="in"
    )

    class Meta:
        model = RegionConfigurationAreaModel
        fields = [
            "area_id",
            "pincode_id",
            "city_id",
            "zone_id",
            "region_id",
        ]
