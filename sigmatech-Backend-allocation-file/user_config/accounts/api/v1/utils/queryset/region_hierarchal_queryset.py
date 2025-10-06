"""
Utilities for filtering region, zone, city, pincode, and area querysets
based on user role and reporting hierarchy.

This module enforces role-based access control (RBAC) on hierarchical location data
(regions, zones, cities, pincodes, areas). Each function filters querysets to ensure
users (Admin, Sr. Manager, Manager, Supervisor, or Field Officer) only access data
they are authorized to view based on their role and reporting hierarchy.
"""

from core_utils.utils.global_variables import STATUS_ACTIVATED_GLOBAL_FILTERSET
from store.configurations.region_config.models import (
    RegionConfigurationAreaModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
)
from django.db.models.query import QuerySet
from user_config.accounts.models import UserDetailModel
from user_config.user_auth.models import UserModel
from user_config.user_auth.enums import UserRoleEnum
from django.db.models.query_utils import Q
from typing import Dict, List, Optional

# Role access rules by hierarchy level
# Defines which roles can access each level of the location hierarchy
REGION_LEVEL_USER_ROLE_GLOBAL: Dict[str, List] = {
    "region": [UserRoleEnum.ADMIN.value, UserRoleEnum.SR_MANAGER.value],
    "zone": [
        UserRoleEnum.ADMIN.value,
        UserRoleEnum.SR_MANAGER.value,
        UserRoleEnum.MANAGER.value,
    ],
    "city": [
        UserRoleEnum.ADMIN.value,
        UserRoleEnum.SR_MANAGER.value,
        UserRoleEnum.MANAGER.value,
        UserRoleEnum.SUPERVISOR.value,
    ],
    "pincode": [
        UserRoleEnum.ADMIN.value,
        UserRoleEnum.SR_MANAGER.value,
        UserRoleEnum.MANAGER.value,
        UserRoleEnum.SUPERVISOR.value,
        UserRoleEnum.FIELD_OFFICER.value,
    ],
}


def get_reporting_users(
    user_instance: UserModel,
    user_detail_queryset: QuerySet = UserDetailModel.objects.all(),
    status_filterset: Dict = STATUS_ACTIVATED_GLOBAL_FILTERSET,
) -> QuerySet[UserDetailModel]:
    """
    Retrieves a queryset of UserDetailModel instances for the given user and their direct reports.

    This function identifies users who report to the provided user_instance (e.g., subordinates)
    or the user themselves, ensuring only active users (based on status_filterset) are included.

    Args:
        user_instance (UserModel): The user for whom reporting users are fetched.
        user_detail_queryset (QuerySet, optional): Base queryset of UserDetailModel to filter. Defaults to all UserDetailModel objects.
        status_filterset (Dict, optional): Filter dictionary to ensure only active records are returned. Defaults to STATUS_ACTIVATED_GLOBAL_FILTERSET.

    Returns:
        QuerySet[UserDetailModel]: Filtered queryset containing user details for the user and their direct reports.
    """
    return user_detail_queryset.filter(**status_filterset).filter(
        Q(user__reports_to=user_instance) | Q(user=user_instance)
    )


def get_user_assigned_region_queryset(
    user_instance: UserModel,
    queryset: QuerySet[
        RegionConfigurationRegionModel
    ] = RegionConfigurationRegionModel.objects.all(),
) -> QuerySet[RegionConfigurationRegionModel]:
    """
    Retrieves a queryset of regions that the user is authorized to access.

    Access Rules:
        - Admins: Have access to all active regions.
        - Other roles: Only access regions explicitly assigned to them or their direct reports.

    Args:
        user_instance (UserModel): The user whose assigned regions are being retrieved.
        queryset (QuerySet): Base queryset of RegionConfigurationRegionModel to filter. Defaults to all regions.

    Returns:
        QuerySet[RegionConfigurationRegionModel]: Filtered queryset of regions the user can access.
    """
    if user_instance.user_role.role != UserRoleEnum.ADMIN.value:
        # Non-admins are restricted to regions assigned to them or their direct reports
        user_detail_queryset = get_reporting_users(user_instance=user_instance)
        queryset = queryset.filter(
            pk__in=user_detail_queryset.values_list("assigned_region", flat=True)
        )
    return queryset.filter(**STATUS_ACTIVATED_GLOBAL_FILTERSET)


def get_user_assigned_zone_queryset(
    user_instance: UserModel,
    queryset: QuerySet[
        RegionConfigurationZoneModel
    ] = RegionConfigurationZoneModel.objects.all(),
    region: List[str] = [],
) -> QuerySet[RegionConfigurationZoneModel]:
    """
    Retrieves a queryset of zones that the user is authorized to access, optionally filtered by specific regions.

    Access Rules:
        - Admins: Access all active zones.
        - Sr. Managers and Managers: Access zones assigned to their direct reports or themselves.
        - Other roles: No access (returns empty queryset unless explicitly assigned).

    Args:
        user_instance (UserModel): The user whose assigned zones are being retrieved.
        queryset (QuerySet): Base queryset of RegionConfigurationZoneModel to filter. Defaults to all zones.
        region (List[str]): Optional list of region IDs to further filter the zones.

    Returns:
        QuerySet[RegionConfigurationZoneModel]: Filtered queryset of zones the user can access.
    """
    region_filterset: Dict = {}

    if user_instance.user_role.role == UserRoleEnum.ADMIN.value:
        # Admins have unrestricted access to all active zones
        zone_queryset = queryset.all()
    elif user_instance.user_role.role == UserRoleEnum.SR_MANAGER.value:
        user_detail_queryset = get_reporting_users(user_instance=user_instance)
        zone_queryset = queryset.filter(
            region__pk__in=user_detail_queryset.values_list(
                "assigned_region", flat=True
            )
        )
    else:
        # Non-admins (e.g., Sr. Manager, Manager) access zones assigned to their reporting users
        user_detail_queryset = get_reporting_users(user_instance=user_instance)

        zone_queryset = queryset.filter(
            pk__in=user_detail_queryset.values_list("assigned_zone", flat=True)
        )

    if region:
        # Apply region filter if provided
        region_filterset["region__pk__in"] = region
    return zone_queryset.filter(**region_filterset)


def get_user_assigned_city_queryset(
    user_instance: UserModel,
    queryset: QuerySet[
        RegionConfigurationCityModel
    ] = RegionConfigurationCityModel.objects.all(),
    zone: Optional[List[str]] = [],
) -> QuerySet[RegionConfigurationCityModel]:
    """
    Retrieves a queryset of cities that the user is authorized to access.

    Access Rules:
        - Managers: Access cities linked to their assigned zones.
        - Supervisors: Access cities explicitly assigned to them in UserDetail.
        - Field Officers: Access cities explicitly assigned to them in UserDetail.
        - Other roles: No access (returns empty queryset).

    Args:
        user_instance (UserModel): The user whose assigned cities are being retrieved.
        queryset (QuerySet): Base queryset of RegionConfigurationCityModel to filter. Defaults to all cities.

    Returns:
        QuerySet[RegionConfigurationCityModel]: Filtered queryset of cities the user can access.
    """
    filter_set: Dict = {}
    assigned_zone_queryset: QuerySet[RegionConfigurationZoneModel] = (
        get_user_assigned_zone_queryset(user_instance=user_instance)
    )
    zone_filters: Dict = {}
    if zone:
        zone_filters["zone__pk__in"] = zone

    if user_instance.user_role.role == UserRoleEnum.MANAGER.value:
        # Managers access cities within their assigned zones
        filter_set["zone__pk__in"] = assigned_zone_queryset.values_list("pk", flat=True)

    elif user_instance.user_role.role == UserRoleEnum.SUPERVISOR.value:
        # Supervisors access cities explicitly assigned to them or their reports
        user_detail_queryset = get_reporting_users(user_instance=user_instance)
        filter_set["pk__in"] = user_detail_queryset.values_list(
            "assigned_city", flat=True
        )

    elif user_instance.user_role.role == UserRoleEnum.FIELD_OFFICER.value:
        # Field Officers access only their directly assigned cities
        filter_set[
            "pk__in"
        ] = user_instance.UserDetailModel_user.assigned_city.all().values_list(
            "pk", flat=True
        )

    return queryset.filter(**filter_set).filter(**zone_filters)


def get_user_assigned_pincode_queryset(
    user_instance: UserModel,
    queryset: QuerySet[
        RegionConfigurationPincodeModel
    ] = RegionConfigurationPincodeModel.objects.all(),
    city: List[str] = [],
) -> QuerySet[RegionConfigurationPincodeModel]:
    """
    Retrieves a queryset of pincodes that the user is authorized to access, optionally filtered by specific cities.

    Access Rules:
        - Managers and Supervisors: Access pincodes within their assigned cities.
        - Field Officers: Access pincodes explicitly assigned to them in UserDetail.
        - Other roles: No access (returns empty queryset).

    Args:
        user_instance (UserModel): The user whose assigned pincodes are being retrieved.
        queryset (QuerySet): Base queryset of RegionConfigurationPincodeModel to filter. Defaults to all pincodes.
        city (List[str]): Optional list of city IDs to further filter the pincodes.

    Returns:
        QuerySet[RegionConfigurationPincodeModel]: Filtered queryset of pincodes the user can access.
    """
    filter_set: Dict = {}
    assigned_city_queryset: QuerySet[RegionConfigurationCityModel] = (
        get_user_assigned_city_queryset(user_instance=user_instance)
    )

    # Apply city filter if provided
    if city:
        queryset: QuerySet[RegionConfigurationCityModel] = queryset.filter(
            city__pk__in=city
        )

    if user_instance.user_role.role == UserRoleEnum.MANAGER.value:
        # Managers and Supervisors access pincodes within their assigned cities
        filter_set["city__pk__in"] = assigned_city_queryset.values_list("pk", flat=True)
    elif user_instance.user_role.role == UserRoleEnum.SUPERVISOR.value:
        if user_instance.UserDetailModel_user.assigned_pincode.all().exists():
            filter_set[
                "pk__in"
            ] = user_instance.UserDetailModel_user.assigned_pincode.all().values_list(
                "pk", flat=True
            )
        else:
            filter_set["city__pk__in"] = assigned_city_queryset.values_list(
                "pk", flat=True
            )

    elif user_instance.user_role.role == UserRoleEnum.FIELD_OFFICER.value:
        # Field Officers access only their directly assigned pincodes
        filter_set[
            "pk__in"
        ] = user_instance.UserDetailModel_user.assigned_pincode.all().values_list(
            "pk", flat=True
        )

    return queryset.filter(**STATUS_ACTIVATED_GLOBAL_FILTERSET, **filter_set)


def get_user_assigned_area_queryset(
    user_instance: UserModel,
    queryset: QuerySet[
        RegionConfigurationAreaModel
    ] = RegionConfigurationAreaModel.objects.all(),
    pincode: List[str] = None,
) -> QuerySet[RegionConfigurationAreaModel]:
    """
    Retrieves a queryset of areas that the user is authorized to access, optionally filtered by specific pincodes.

    Access Rules:
        - Managers and Supervisors: Access areas within their assigned pincodes.
        - Field Officers: Access areas explicitly assigned to them in UserDetail.
        - Other roles: No access (returns empty queryset).

    Args:
        user_instance (UserModel): The user whose assigned areas are being retrieved.
        queryset (QuerySet): Base queryset of RegionConfigurationAreaModel to filter. Defaults to all areas.
        pincode (List[str]): Optional list of pincode IDs to further filter the areas.

    Returns:
        QuerySet[RegionConfigurationAreaModel]: Filtered queryset of areas the user can access.
    """
    filter_set: Dict = {}
    assigned_pincode_queryset = get_user_assigned_pincode_queryset(
        user_instance=user_instance
    )

    # Apply pincode filter if provided
    if pincode:
        queryset = queryset.filter(pincode__pk__in=pincode)

    if user_instance.user_role.role == UserRoleEnum.MANAGER.value:
        # Managers and Supervisors access areas within their assigned pincodes
        filter_set["pincode__pk__in"] = assigned_pincode_queryset.values_list(
            "pk", flat=True
        )
    elif user_instance.user_role.role == UserRoleEnum.SUPERVISOR.value:
        if user_instance.UserDetailModel_user.assigned_area.all().exists():
            filter_set[
                "pk__in"
            ] = user_instance.UserDetailModel_user.assigned_area.all().values_list(
                "pk", flat=True
            )
        else:
            filter_set["pincode__pk__in"] = assigned_pincode_queryset.values_list(
                "pk", flat=True
            )

    elif user_instance.user_role.role == UserRoleEnum.FIELD_OFFICER.value:
        # Field Officers access only their directly assigned areas
        filter_set[
            "pk__in"
        ] = user_instance.UserDetailModel_user.assigned_area.all().values_list(
            "pk", flat=True
        )

    return queryset.filter(**STATUS_ACTIVATED_GLOBAL_FILTERSET, **filter_set)
