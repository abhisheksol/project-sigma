from django.core.management.base import BaseCommand

from store.configurations.region_config.models import (
    RegionConfigurationCityModel,
    RegionConfigurationZoneModel,
)
from user_config.accounts.models import UserDetailModel
from user_config.user_auth.enums import UserRoleEnum
from user_config.user_auth.models import UserModel
from django.db.models import Subquery, OuterRef
from django.db.models import Case, When
from django.db.models import Subquery, OuterRef, Case, When

from django.db.models import OuterRef, Subquery, Value, Case, When, F, query
from django.db.models import OuterRef, Subquery, Value, UUIDField, Case, When, F


def get_user_queryset():
    # FIELD_OFFICER / SUPERVISOR: get city -> zone -> region PKs
    city_id_qs = UserDetailModel.assigned_city.through.objects.filter(
        userdetailmodel_id=OuterRef("pk")
    ).values("regionconfigurationcitymodel_id")[
        :1
    ]  # city PK

    zone_id_from_city_qs = RegionConfigurationCityModel.objects.filter(
        id=OuterRef("UserDetailModel_user__assigned_city__id")
    ).values("zone_id")[:1]

    region_id_from_city_qs = RegionConfigurationCityModel.objects.filter(
        id=OuterRef("UserDetailModel_user__assigned_city__id")
    ).values("zone__region_id")[:1]

    # MANAGER: get zone -> region PK
    region_id_from_zone_qs = RegionConfigurationZoneModel.objects.filter(
        id=OuterRef("UserDetailModel_user__assigned_zone__id")
    ).values("region_id")[:1]

    qs: query.QuerySet[UserModel] = UserModel.objects.select_related(
        "user_role"
    ).annotate(
        city_id=Case(
            When(
                user_role__role__in=[
                    UserRoleEnum.FIELD_OFFICER,
                    UserRoleEnum.SUPERVISOR,
                ],
                then=Subquery(city_id_qs),
            ),
            default=Value(None),
            output_field=UUIDField(),
        ),
        zone_id=Case(
            When(
                user_role__role__in=[
                    UserRoleEnum.FIELD_OFFICER,
                    UserRoleEnum.SUPERVISOR,
                ],
                then=Subquery(zone_id_from_city_qs),
            ),
            When(
                user_role__role=UserRoleEnum.MANAGER,
                then=F("UserDetailModel_user__assigned_zone__id"),
            ),
            default=Value(None),
            output_field=UUIDField(),
        ),
        region_id=Case(
            When(
                user_role__role__in=[
                    UserRoleEnum.FIELD_OFFICER,
                    UserRoleEnum.SUPERVISOR,
                ],
                then=Subquery(region_id_from_city_qs),
            ),
            When(
                user_role__role=UserRoleEnum.MANAGER,
                then=Subquery(region_id_from_zone_qs),
            ),
            When(
                user_role__role=UserRoleEnum.SR_MANAGER,
                then=F("UserDetailModel_user__assigned_region__id"),
            ),
            default=Value(None),
            output_field=UUIDField(),
        ),
    )

    return qs


class Command(BaseCommand):
    help: str = "Playground Shell"

    def handle(self, *args, **kwargs):
        region: str = "d03fa54d-97ac-11f0-889e-00155dc55716"
        zone: str = "d0406202-97ac-11f0-bb32-00155dc55716"

        queryset = UserDetailModel.objects.all()
        if region:
            queryset = queryset.filter_by_region(region)
            print("region", region, queryset)
        if zone:
            queryset = queryset.filter_by_zone(zone)
            print("zone", zone, queryset)
        print(queryset)
