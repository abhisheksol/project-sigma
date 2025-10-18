from django.core.management.base import BaseCommand
from django.db import transaction
from typing import List
from django.db.models.query import QuerySet

from core_utils.region_data.models import PincodeModel
from store.configurations.region_config.models import (
    RegionConfigurationAreaModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
)


def load_pincode(pincode_instance: PincodeModel) -> RegionConfigurationPincodeModel:
    if RegionConfigurationPincodeModel.objects.filter(
        pincode=pincode_instance
    ).exists():
        return pincode_instance.RegionConfigurationPincodeModel_pincode
    region: str = pincode_instance.country.name
    state: str = pincode_instance.state.name
    city: str = (
        pincode_instance.division_name
        if pincode_instance.division_name
        else (
            pincode_instance.circle_name
            if pincode_instance.circle_name
            else pincode_instance.district
        )
    )
    if not region or not state or not city:
        return
    region_instance, _ = RegionConfigurationRegionModel.objects.get_or_create(
        title=region
    )
    zone_instance, _ = RegionConfigurationZoneModel.objects.get_or_create(
        title=state, region=region_instance
    )
    city_instance, _ = RegionConfigurationCityModel.objects.get_or_create(
        city_name=city, zone=zone_instance
    )

    region_pincode_instance, _ = RegionConfigurationPincodeModel.objects.get_or_create(
        pincode=pincode_instance, city=city_instance
    )

    area: str = (
        pincode_instance.circle_name
        if pincode_instance.circle_name
        else pincode_instance.district
    )
    if not RegionConfigurationAreaModel.objects.filter(
        title=area, pincode=region_pincode_instance
    ).exists():
        if area:
            RegionConfigurationAreaModel.objects.get_or_create(
                title=area, pincode=region_pincode_instance
            )

    return region_pincode_instance


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        pincodes: List[str] = [
            500050,
            502032,
            502032,
            500049,
            500019,
            502032,
            500050,
            500050,
            502032,
            500050,
            500050,
            502032,
            500050,
            500050,
            500050,
            500050,
            500050,
            500050,
            502302,
            500050,
            500049,
            500050,
            500019,
            500050,
            500050,
            500049,
            500050,
            500050,
            500050,
            502032,
        ]
        # pincode_queryset: QuerySet[PincodeModel] = PincodeModel.objects.all().filter(
        #     pincode__in=pincodes
        # )

        # for query in pincode_queryset:
        #     load_pincode(pincode_instance=query)
        pincode_queryset: QuerySet[PincodeModel] = PincodeModel.objects.all()
        with transaction.atomic():
            for query in pincode_queryset:
                region_pincode_instance: RegionConfigurationPincodeModel = load_pincode(
                    pincode_instance=query
                )
                if region_pincode_instance:
                    print(region_pincode_instance.pincode.pincode, "loaded")
