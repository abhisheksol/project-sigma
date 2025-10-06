from typing import List
from django.db.models.query import QuerySet

from store.configurations.region_config.models import (
    RegionConfigurationAreaModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
)
from user_config.user_auth.models import UserModel
from user_config.user_auth.enums import UserRoleEnum


def get_user_instance_assigned_region_queryset(
    user_instance: UserModel,
) -> QuerySet[RegionConfigurationRegionModel]:
    """
    Retrieve all regions assigned to a given user, based on their role.

    - ADMIN: No regions assigned (returns empty queryset).
    - SR_MANAGER: Returns directly assigned regions.
    - MANAGER: Returns regions derived from assigned zones.
    - SUPERVISOR / FIELD_OFFICER: Returns regions derived from cities, pincodes, or areas.
    - Others: Returns empty queryset.

    Args:
        user_instance (UserModel): The user instance whose assigned regions need to be fetched.

    Returns:
        QuerySet[RegionConfigurationRegionModel]: A queryset of assigned regions.
    """
    role: str = user_instance.user_role.role

    if role == UserRoleEnum.ADMIN.value:
        return RegionConfigurationRegionModel.objects.none()

    if role == UserRoleEnum.SR_MANAGER.value:
        return user_instance.UserDetailModel_user.assigned_region.all()

    if role == UserRoleEnum.MANAGER.value:
        region_ids: List[str] = list(
            user_instance.UserDetailModel_user.assigned_zone.values_list(
                "region__pk", flat=True
            )
        )
        return RegionConfigurationRegionModel.objects.filter(pk__in=region_ids)

    if role in [UserRoleEnum.SUPERVISOR.value, UserRoleEnum.FIELD_OFFICER.value]:
        # Collect all possible region IDs from assigned city, pincode, and area levels
        city_region_ids: List[str] = list(
            user_instance.UserDetailModel_user.assigned_city.values_list(
                "zone__region__pk", flat=True
            )
        )
        pincode_region_ids: List[str] = list(
            user_instance.UserDetailModel_user.assigned_pincode.values_list(
                "city__zone__region__pk", flat=True
            )
        )
        area_region_ids: List[str] = list(
            user_instance.UserDetailModel_user.assigned_area.values_list(
                "pincode__city__zone__region__pk", flat=True
            )
        )

        combined_ids: List[str] = city_region_ids + pincode_region_ids + area_region_ids
        return (
            RegionConfigurationRegionModel.objects.filter(
                pk__in=combined_ids
            ).distinct()
            if combined_ids
            else RegionConfigurationRegionModel.objects.none()
        )

    return RegionConfigurationRegionModel.objects.none()


def get_user_instance_assigned_zone_queryset(
    user_instance: UserModel,
) -> QuerySet[RegionConfigurationZoneModel]:
    """
    Retrieve all zones assigned to a given user, based on their role.

    - ADMIN / SR_MANAGER: No zones assigned (returns empty queryset).
    - MANAGER: Returns directly assigned zones.
    - SUPERVISOR / FIELD_OFFICER: Returns zones derived from cities, pincodes, or areas.
    - Others: Returns empty queryset.

    Args:
        user_instance (UserModel): The user instance whose assigned zones need to be fetched.

    Returns:
        QuerySet[RegionConfigurationZoneModel]: A queryset of assigned zones.
    """
    role: str = user_instance.user_role.role

    if role in [UserRoleEnum.ADMIN.value, UserRoleEnum.SR_MANAGER.value]:
        return RegionConfigurationZoneModel.objects.none()

    if role == UserRoleEnum.MANAGER.value:
        return user_instance.UserDetailModel_user.assigned_zone.all()

    if role in [UserRoleEnum.SUPERVISOR.value, UserRoleEnum.FIELD_OFFICER.value]:
        city_zone_ids: List[str] = list(
            user_instance.UserDetailModel_user.assigned_city.values_list(
                "zone__pk", flat=True
            )
        )
        pincode_zone_ids: List[str] = list(
            user_instance.UserDetailModel_user.assigned_pincode.values_list(
                "city__zone__pk", flat=True
            )
        )
        area_zone_ids: List[str] = list(
            user_instance.UserDetailModel_user.assigned_area.values_list(
                "pincode__city__zone__pk", flat=True
            )
        )

        combined_ids: List[str] = city_zone_ids + pincode_zone_ids + area_zone_ids
        return (
            RegionConfigurationZoneModel.objects.filter(pk__in=combined_ids).distinct()
            if combined_ids
            else RegionConfigurationZoneModel.objects.none()
        )

    return RegionConfigurationZoneModel.objects.none()


def get_user_instance_assigned_city_queryset(
    user_instance: UserModel,
) -> QuerySet[RegionConfigurationCityModel]:
    """
    Retrieve all cities assigned to a given user, based on their role.

    - ADMIN / SR_MANAGER / MANAGER: No cities assigned (returns empty queryset).
    - SUPERVISOR / FIELD_OFFICER: Returns cities derived from direct assignment, pincodes, or areas.
    - Others: Returns empty queryset.

    Args:
        user_instance (UserModel): The user instance whose assigned cities need to be fetched.

    Returns:
        QuerySet[RegionConfigurationCityModel]: A queryset of assigned cities.
    """
    role: str = user_instance.user_role.role

    if role in [
        UserRoleEnum.ADMIN.value,
        UserRoleEnum.SR_MANAGER.value,
        UserRoleEnum.MANAGER.value,
    ]:
        return RegionConfigurationCityModel.objects.none()

    if role in [UserRoleEnum.SUPERVISOR.value, UserRoleEnum.FIELD_OFFICER.value]:
        city_ids: List[str] = list(
            user_instance.UserDetailModel_user.assigned_city.values_list(
                "pk", flat=True
            )
        )
        pincode_city_ids: List[str] = list(
            user_instance.UserDetailModel_user.assigned_pincode.values_list(
                "city__pk", flat=True
            )
        )
        area_city_ids: List[str] = list(
            user_instance.UserDetailModel_user.assigned_area.values_list(
                "pincode__city__pk", flat=True
            )
        )

        combined_ids: List[str] = city_ids + pincode_city_ids + area_city_ids
        return (
            RegionConfigurationCityModel.objects.filter(pk__in=combined_ids).distinct()
            if combined_ids
            else RegionConfigurationCityModel.objects.none()
        )

    return RegionConfigurationCityModel.objects.none()


def get_user_instance_assigned_pincode_queryset(
    user_instance: UserModel,
) -> QuerySet[RegionConfigurationPincodeModel]:
    """
    Retrieve all pincodes assigned to a given user, based on their role.

    - ADMIN / SR_MANAGER / MANAGER: No pincodes assigned (returns empty queryset).
    - SUPERVISOR / FIELD_OFFICER: Returns pincodes derived from direct assignment or areas.
    - Others: Returns empty queryset.

    Args:
        user_instance (UserModel): The user instance whose assigned pincodes need to be fetched.

    Returns:
        QuerySet[RegionConfigurationPincodeModel]: A queryset of assigned pincodes.
    """
    role: str = user_instance.user_role.role

    if role in [
        UserRoleEnum.ADMIN.value,
        UserRoleEnum.SR_MANAGER.value,
        UserRoleEnum.MANAGER.value,
    ]:
        return RegionConfigurationPincodeModel.objects.none()

    if role in [UserRoleEnum.SUPERVISOR.value, UserRoleEnum.FIELD_OFFICER.value]:
        pincode_ids: List[str] = list(
            user_instance.UserDetailModel_user.assigned_pincode.values_list(
                "pk", flat=True
            )
        )
        area_pincode_ids: List[str] = list(
            user_instance.UserDetailModel_user.assigned_area.values_list(
                "pincode__pk", flat=True
            )
        )

        combined_ids: List[str] = pincode_ids + area_pincode_ids
        return (
            RegionConfigurationPincodeModel.objects.filter(
                pk__in=combined_ids
            ).distinct()
            if combined_ids
            else RegionConfigurationPincodeModel.objects.none()
        )

    return RegionConfigurationPincodeModel.objects.none()


def get_user_instance_assigned_area_queryset(
    user_instance: UserModel,
) -> QuerySet[RegionConfigurationAreaModel]:
    """
    Retrieve all areas assigned to a given user, based on their role.

    - ADMIN / SR_MANAGER / MANAGER: No areas assigned (returns empty queryset).
    - SUPERVISOR / FIELD_OFFICER: Returns directly assigned areas.
    - Others: Returns empty queryset.

    Args:
        user_instance (UserModel): The user instance whose assigned areas need to be fetched.

    Returns:
        QuerySet[RegionConfigurationAreaModel]: A queryset of assigned areas.
    """
    role: str = user_instance.user_role.role

    if role in [
        UserRoleEnum.ADMIN.value,
        UserRoleEnum.SR_MANAGER.value,
        UserRoleEnum.MANAGER.value,
    ]:
        return RegionConfigurationAreaModel.objects.none()

    if role in [UserRoleEnum.SUPERVISOR.value, UserRoleEnum.FIELD_OFFICER.value]:
        return user_instance.UserDetailModel_user.assigned_area.all()

    return RegionConfigurationAreaModel.objects.none()
