from typing import Dict
from django.db.models.query import QuerySet
from store.configurations.region_config.models import (
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationAreaModel,
)
from user_config.accounts.models import UserDetailModel


def unassigned_region_for_user_queryset(
    filter_set: Dict = {},
) -> QuerySet[RegionConfigurationRegionModel]:
    """
    Returns a queryset of regions that are not assigned to any user.

    This function retrieves all regions that are not linked to any UserDetailModel
    via the assigned_region ManyToManyField. The user_instance parameter is included
    for consistency with other functions but is not used in the logic.

    Args:
        user_instance (UserModel, optional): The user instance (not used in logic but included for API consistency).
        filter_set (Dict, optional): Additional filters to apply to the queryset. Defaults to {}.

    Returns:
        QuerySet[RegionConfigurationRegionModel]: Queryset of unassigned regions.
    """
    # Use prefetch_related to optimize fetching of assigned_region ManyToManyField
    return RegionConfigurationRegionModel.objects.exclude(
        pk__in=UserDetailModel.objects.prefetch_related("assigned_region").values_list(
            "assigned_region__pk", flat=True
        )
    ).filter(**filter_set)


def unassigned_zone_for_user_queryset(
    filter_set: Dict = {},
) -> QuerySet[RegionConfigurationZoneModel]:
    """
    Returns a queryset of zones that are not assigned to any user.

    This function retrieves all zones that are not linked to any UserDetailModel
    via the assigned_zone ManyToManyField. The user_instance parameter is included
    for consistency with other functions but is not used in the logic.

    Args:
        user_instance (UserModel, optional): The user instance (not used in logic but included for API consistency).
        filter_set (Dict, optional): Additional filters to apply to the queryset. Defaults to {}.

    Returns:
        QuerySet[RegionConfigurationZoneModel]: Queryset of unassigned zones.
    """
    # Use prefetch_related to optimize fetching of assigned_zone ManyToManyField
    return (
        RegionConfigurationZoneModel.objects.exclude(
            pk__in=UserDetailModel.objects.prefetch_related(
                "assigned_zone"
            ).values_list("assigned_zone__pk", flat=True)
        )
        .select_related("region")
        .filter(**filter_set)
    )


def unassigned_city_for_user_queryset(
    filter_set: Dict = {},
) -> QuerySet[RegionConfigurationCityModel]:
    """
    Returns a queryset of cities that are not assigned to any user.

    This function retrieves all cities that are not linked to any UserDetailModel
    via the assigned_city ManyToManyField. The user_instance parameter is included
    for consistency with other functions but is not used in the logic.

    Args:
        user_instance (UserModel, optional): The user instance (not used in logic but included for API consistency).
        filter_set (Dict, optional): Additional filters to apply to the queryset. Defaults to {}.

    Returns:
        QuerySet[RegionConfigurationCityModel]: Queryset of unassigned cities.
    """
    # Use prefetch_related to optimize fetching of assigned_city ManyToManyField
    return (
        RegionConfigurationCityModel.objects.exclude(
            pk__in=UserDetailModel.objects.prefetch_related(
                "assigned_city"
            ).values_list("assigned_city__pk", flat=True)
        )
        .select_related("zone", "city_name")
        .filter(**filter_set)
    )


def unassigned_pincode_for_user_queryset(
    filter_set: Dict = {},
) -> QuerySet[RegionConfigurationPincodeModel]:
    """
    Returns a queryset of pincodes that are not assigned to any user.

    This function retrieves all pincodes that are not linked to any UserDetailModel
    via the assigned_pincode ManyToManyField. The user_instance parameter is included
    for consistency with other functions but is not used in the logic.

    Args:
        user_instance (UserModel, optional): The user instance (not used in logic but included for API consistency).
        filter_set (Dict, optional): Additional filters to apply to the queryset. Defaults to {}.

    Returns:
        QuerySet[RegionConfigurationPincodeModel]: Queryset of unassigned pincodes.
    """
    # Use prefetch_related to optimize fetching of assigned_pincode ManyToManyField
    return (
        RegionConfigurationPincodeModel.objects.exclude(
            pk__in=UserDetailModel.objects.prefetch_related(
                "assigned_pincode"
            ).values_list("assigned_pincode__pk", flat=True)
        )
        .select_related("city", "pincode")
        .filter(**filter_set)
    )


def unassigned_area_for_user_queryset(
    filter_set: Dict = {},
) -> QuerySet[RegionConfigurationAreaModel]:
    """
    Returns a queryset of areas that are not assigned to any user.

    This function retrieves all areas that are not linked to any UserDetailModel
    via the assigned_area ManyToManyField. The user_instance parameter is included
    for consistency with other functions but is not used in the logic.

    Args:
        user_instance (UserModel, optional): The user instance (not used in logic but included for API consistency).
        filter_set (Dict, optional): Additional filters to apply to the queryset. Defaults to {}.

    Returns:
        QuerySet[RegionConfigurationAreaModel]: Queryset of unassigned areas.
    """
    # Use prefetch_related to optimize fetching of assigned_area ManyToManyField
    return (
        RegionConfigurationAreaModel.objects.exclude(
            pk__in=UserDetailModel.objects.prefetch_related(
                "assigned_area"
            ).values_list("assigned_area__pk", flat=True)
        )
        .select_related("pincode")
        .filter(**filter_set)
    )
