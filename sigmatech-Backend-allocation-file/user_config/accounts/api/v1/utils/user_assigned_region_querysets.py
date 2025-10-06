from typing import Dict
from django.db.models.query import QuerySet
from user_config.user_auth.enums import UserRoleEnum
from user_config.user_auth.models import UserModel
from store.configurations.region_config.models import (
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationAreaModel,
)
from user_config.accounts.models import UserDetailModel


def assigned_region_for_user_queryset(
    user_instance: UserModel, filter_set: Dict = {}
) -> QuerySet[RegionConfigurationRegionModel]:
    """
    Returns a queryset of regions accessible to the user based on their role.

    For Admins, returns all regions. For Senior Managers, returns their assigned regions.
    Other roles receive an empty queryset.

    Args:
        user_instance (UserModel): The user instance to check permissions for.
        filter_set (Dict, optional): Additional filters to apply to the queryset. Defaults to {}.

    Returns:
        QuerySet[RegionConfigurationRegionModel]: Queryset of accessible regions.

    Raises:
        UserDetailModel.DoesNotExist: If the user has no associated UserDetailModel (handled internally).
    """
    try:
        user_detail_instance: UserDetailModel = user_instance.UserDetailModel_user
    except UserDetailModel.DoesNotExist:
        return RegionConfigurationRegionModel.objects.none()

    if UserRoleEnum.ADMIN.value == user_instance.user_role:
        return RegionConfigurationRegionModel.objects.all().filter(**filter_set)
    if UserRoleEnum.SR_MANAGER.value == user_instance.user_role:
        # Prefetch related regions to optimize ManyToManyField access
        return user_detail_instance.assigned_region.all().filter(**filter_set)
    return RegionConfigurationRegionModel.objects.none()


def assigned_zone_for_user_queryset(
    user_instance: UserModel, filter_set: Dict = {}
) -> QuerySet[RegionConfigurationZoneModel]:
    """
    Returns a queryset of zones accessible to the user based on their role.

    For Admins, returns all zones. For Senior Managers, returns zones under their assigned regions.
    For Managers, returns their assigned zones. Other roles receive an empty queryset.

    Args:
        user_instance (UserModel): The user instance to check permissions for.
        filter_set (Dict, optional): Additional filters to apply to the queryset. Defaults to {}.

    Returns:
        QuerySet[RegionConfigurationZoneModel]: Queryset of accessible zones.

    Raises:
        UserDetailModel.DoesNotExist: If the user has no associated UserDetailModel (handled internally).
    """
    try:
        user_detail_instance: UserDetailModel = user_instance.UserDetailModel_user
    except UserDetailModel.DoesNotExist:
        return RegionConfigurationZoneModel.objects.none()

    if UserRoleEnum.ADMIN.value == user_instance.user_role:
        return RegionConfigurationZoneModel.objects.all().filter(**filter_set)
    if UserRoleEnum.SR_MANAGER.value == user_instance.user_role:
        # Optimize by prefetching regions for senior managers
        return (
            RegionConfigurationZoneModel.objects.filter(
                region__pk__in=user_detail_instance.assigned_region.all().values_list(
                    "pk", flat=True
                )
            )
            .select_related("region")
            .filter(**filter_set)
        )
    elif UserRoleEnum.MANAGER.value == user_instance.user_role:
        # Prefetch assigned zones to optimize ManyToManyField access
        return (
            user_detail_instance.assigned_zone.all()
            .select_related("region")
            .filter(**filter_set)
        )
    return RegionConfigurationZoneModel.objects.none()


def assigned_city_for_user_queryset(
    user_instance: UserModel, filter_set: Dict = {}
) -> QuerySet[RegionConfigurationCityModel]:
    """
    Returns a queryset of cities accessible to the user based on their role.

    For Admins, returns all cities. For Senior Managers, returns cities under their regions.
    For Managers, returns cities under their zones. For Supervisors, returns their assigned cities.
    Other roles receive an empty queryset.

    Args:
        user_instance (UserModel): The user instance to check permissions for.
        filter_set (Dict, optional): Additional filters to apply to the queryset. Defaults to {}.

    Returns:
        QuerySet[RegionConfigurationCityModel]: Queryset of accessible cities.

    Raises:
        UserDetailModel.DoesNotExist: If the user has no associated UserDetailModel (handled internally).
    """
    try:
        user_detail_instance: UserDetailModel = user_instance.UserDetailModel_user
    except UserDetailModel.DoesNotExist:
        return RegionConfigurationCityModel.objects.none()

    if UserRoleEnum.ADMIN.value == user_instance.user_role:
        return RegionConfigurationCityModel.objects.all().filter(**filter_set)
    if UserRoleEnum.SR_MANAGER.value == user_instance.user_role:
        # Optimize by prefetching zone and region for senior managers
        return (
            RegionConfigurationCityModel.objects.filter(
                zone__region__pk__in=user_detail_instance.assigned_region.all().values_list(
                    "pk", flat=True
                )
            )
            .select_related("zone__region", "city_name")
            .filter(**filter_set)
        )
    elif UserRoleEnum.MANAGER.value == user_instance.user_role:
        # Optimize by prefetching zone for managers
        return (
            RegionConfigurationCityModel.objects.filter(
                zone__pk__in=user_detail_instance.assigned_zone.all().values_list(
                    "pk", flat=True
                )
            )
            .select_related("zone", "city_name")
            .filter(**filter_set)
        )
    elif UserRoleEnum.SUPERVISOR.value == user_instance.user_role:
        # Prefetch assigned cities to optimize ManyToManyField access
        return (
            user_detail_instance.assigned_city.all()
            .select_related("zone", "city_name")
            .filter(**filter_set)
        )
    return RegionConfigurationCityModel.objects.none()


def assigned_pincode_for_user_queryset(
    user_instance: UserModel, filter_set: Dict = {}
) -> QuerySet[RegionConfigurationPincodeModel]:
    """
    Returns a queryset of pincodes accessible to the user based on their role.

    For Admins, returns all pincodes. For Senior Managers, returns pincodes under their regions.
    For Managers, returns pincodes under their zones. For Supervisors, returns pincodes under their cities.
    For Field Officers, returns their assigned pincodes. Other roles receive an empty queryset.

    Args:
        user_instance (UserModel): The user instance to check permissions for.
        filter_set (Dict, optional): Additional filters to apply to the queryset. Defaults to {}.

    Returns:
        QuerySet[RegionConfigurationPincodeModel]: Queryset of accessible pincodes.

    Raises:
        UserDetailModel.DoesNotExist: If the user has no associated UserDetailModel (handled internally).
    """
    try:
        user_detail_instance: UserDetailModel = user_instance.UserDetailModel_user
    except UserDetailModel.DoesNotExist:
        return RegionConfigurationPincodeModel.objects.none()

    if UserRoleEnum.ADMIN.value == user_instance.user_role:
        return RegionConfigurationPincodeModel.objects.all().filter(**filter_set)
    if UserRoleEnum.SR_MANAGER.value == user_instance.user_role:
        # Optimize by prefetching city, zone, and region for senior managers
        return (
            RegionConfigurationPincodeModel.objects.filter(
                city__zone__region__pk__in=user_detail_instance.assigned_region.all().values_list(
                    "pk", flat=True
                )
            )
            .select_related("city__zone__region", "pincode")
            .filter(**filter_set)
        )
    elif UserRoleEnum.MANAGER.value == user_instance.user_role:
        # Optimize by prefetching city and zone for managers
        return (
            RegionConfigurationPincodeModel.objects.filter(
                city__zone__pk__in=user_detail_instance.assigned_zone.all().values_list(
                    "pk", flat=True
                )
            )
            .select_related("city__zone", "pincode")
            .filter(**filter_set)
        )
    elif UserRoleEnum.SUPERVISOR.value == user_instance.user_role:
        # Optimize by prefetching city for supervisors
        return (
            RegionConfigurationPincodeModel.objects.filter(
                city__pk__in=user_detail_instance.assigned_city.all().values_list(
                    "pk", flat=True
                )
            )
            .select_related("city", "pincode")
            .filter(**filter_set)
        )
    elif UserRoleEnum.FIELD_OFFICER.value == user_instance.user_role:
        # Prefetch assigned pincodes to optimize ManyToManyField access
        return (
            user_detail_instance.assigned_pincode.all()
            .select_related("city", "pincode")
            .filter(**filter_set)
        )
    return RegionConfigurationPincodeModel.objects.none()


def assigned_area_for_user_queryset(
    user_instance: UserModel, filter_set: Dict = {}
) -> QuerySet[RegionConfigurationAreaModel]:
    """
    Returns a queryset of areas accessible to the user based on their role.

    For Admins, returns all areas. For Senior Managers, returns areas under their regions.
    For Managers, returns areas under their zones. For Supervisors, returns areas under their cities.
    For Field Officers, returns their assigned areas. Other roles receive an empty queryset.

    Args:
        user_instance (UserModel): The user instance to check permissions for.
        filter_set (Dict, optional): Additional filters to apply to the queryset. Defaults to {}.

    Returns:
        QuerySet[RegionConfigurationAreaModel]: Queryset of accessible areas.

    Raises:
        UserDetailModel.DoesNotExist: If the user has no associated UserDetailModel (handled internally).
    """
    try:
        user_detail_instance: UserDetailModel = user_instance.UserDetailModel_user
    except UserDetailModel.DoesNotExist:
        return RegionConfigurationAreaModel.objects.none()

    if UserRoleEnum.ADMIN.value == user_instance.user_role:
        return RegionConfigurationAreaModel.objects.all().filter(**filter_set)
    if UserRoleEnum.SR_MANAGER.value == user_instance.user_role:
        # Optimize by prefetching pincode, city, zone, and region for senior managers
        return (
            RegionConfigurationAreaModel.objects.filter(
                pincode__city__zone__region__pk__in=user_detail_instance.assigned_region.all().values_list(
                    "pk", flat=True
                )
            )
            .select_related("pincode__city__zone__region")
            .filter(**filter_set)
        )
    elif UserRoleEnum.MANAGER.value == user_instance.user_role:
        # Optimize by prefetching pincode, city, and zone for managers
        return (
            RegionConfigurationAreaModel.objects.filter(
                pincode__city__zone__pk__in=user_detail_instance.assigned_zone.all().values_list(
                    "pk", flat=True
                )
            )
            .select_related("pincode__city__zone")
            .filter(**filter_set)
        )
    elif UserRoleEnum.SUPERVISOR.value == user_instance.user_role:
        # Optimize by prefetching pincode and city for supervisors
        return (
            RegionConfigurationAreaModel.objects.filter(
                pincode__city__pk__in=user_detail_instance.assigned_city.all().values_list(
                    "pk", flat=True
                )
            )
            .select_related("pincode__city")
            .filter(**filter_set)
        )
    elif UserRoleEnum.FIELD_OFFICER.value == user_instance.user_role:
        # Prefetch assigned areas to optimize ManyToManyField access
        return (
            user_detail_instance.assigned_area.all()
            .select_related("pincode")
            .filter(**filter_set)
        )
    return RegionConfigurationAreaModel.objects.none()
