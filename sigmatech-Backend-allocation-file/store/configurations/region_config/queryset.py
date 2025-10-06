from django.db.models import Count, F, QuerySet


class RegionQuerySet(QuerySet):
    def with_counts(self):
        return self.annotate(
            number_of_zones=Count("RegionConfigurationZoneModel_region", distinct=True),
            number_of_cities=Count(
                "RegionConfigurationZoneModel_region__RegionConfigurationCityModel_zone",
                distinct=True,
            ),
            number_of_pincodes=Count(
                "RegionConfigurationZoneModel_region__RegionConfigurationCityModel_zone__RegionConfigurationPincodeModel_city",
                distinct=True,
            ),
        )


class ZoneQuerySet(QuerySet):
    def with_details(self):
        return self.annotate(
            associated_region=F("region__title"),
            number_of_cities=Count("RegionConfigurationCityModel_zone", distinct=True),
            number_of_pincodes=Count(
                "RegionConfigurationCityModel_zone__RegionConfigurationPincodeModel_city",
                distinct=True,
            ),
            number_of_areas=Count(
                "RegionConfigurationCityModel_zone__RegionConfigurationPincodeModel_city__RegionConfigurationAreaModel_pincode",
                distinct=True,
            ),
        )


class CityQuerySet(QuerySet):
    def with_details(self):
        return self.annotate(
            zone_name=F("zone__title"),
            zone_description=F("zone__description"),
            associated_region=F("zone__region__title"),
            number_of_cities=Count(
                "zone__RegionConfigurationCityModel_zone", distinct=True
            ),
            number_of_pincodes=Count(
                "RegionConfigurationPincodeModel_city", distinct=True
            ),
            number_of_areas=Count(
                "RegionConfigurationPincodeModel_city__RegionConfigurationAreaModel_pincode",
                distinct=True,
            ),
        )


class PincodeQuerySet(QuerySet):
    def with_details(self):
        return self.select_related("city__zone__region").annotate(
            city_name=F("city__city_name"),
            zone_name=F("city__zone__title"),
            region_name=F("city__zone__region__title"),
            area_count=Count("RegionConfigurationAreaModel_pincode"),
            pincode_value=F("pincode"),
        )


class AreaQuerySet(QuerySet):
    def with_details(self):
        return self.select_related(
            "pincode__city__zone__region",  # optimize joins
            "pincode__pincode",  # optimize FK pincode lookup
        ).annotate(
            city_name=F("pincode__city__city_name"),
            zone_name=F("pincode__city__zone__title"),
            region_name=F("pincode__city__zone__region__title"),
            pincode_name=F("pincode__pincode__pincode"),
        )
