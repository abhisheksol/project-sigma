"""
User Management Filtering Utilities

This module provides utility functions to validate query parameters and
filter user querysets based on role-based permissions, hierarchical
reporting, and region-level assignments (region, zone, city, pincode, area).
"""

from typing import Dict, List
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q

from user_config.user_auth.models import UserModel
from user_config.accounts.models import UserDetailModel
from user_config.user_auth.enums import UserRoleEnum
from user_config.accounts.api.v1.utils.queryset.user_reports_to_queryset import (
    get_user_reports_to_queryset,
)

# All region filter keys available
REGION_FILTER_VALUES: List[str] = [
    "assigned_region",
    "assigned_zone",
    "assigned_city",
    "assigned_pincode",
    "assigned_area",
]

RELATIONAL_FILTER_VALUES: Dict[str, List] = {
    "assigned_region": [
        "assigned_zone__region",
        "assigned_city__zone__region",
        "assigned_area__pincode__city__zone__region",
        "assigned_pincode__city__zone__region",
    ],
    "assigned_zone": [
        "assigned_city__zone",
        "assigned_pincode__city__zone",
        "assigned_area__pincode__city__zone",
    ],
    "assigned_city": [
        "assigned_area__pincode__city",
        "assigned_area__pincode__city__zone",
    ],
    "assigned_pincode": ["assigned_area__pincode"],
}

# Dependencies between region filters
# (e.g., zone requires region, city requires region+zone, etc.)
REGION_FILTER_REQUIRED_VALUES: Dict[str, List[str]] = {
    "assigned_region": [],
    "assigned_zone": ["assigned_region"],
    "assigned_city": ["assigned_region", "assigned_zone"],
    "assigned_pincode": ["assigned_region", "assigned_zone", "assigned_city"],
    "assigned_area": [
        "assigned_region",
        "assigned_zone",
        "assigned_city",
        "assigned_pincode",
    ],
}

# Allowed region-level fields for each role
USER_REGION_LEVEL_FIELD: Dict[str, List[str]] = {
    UserRoleEnum.ADMIN.value: REGION_FILTER_VALUES,
    UserRoleEnum.SR_MANAGER.value: [
        "assigned_zone",
        "assigned_city",
        "assigned_pincode",
        "assigned_area",
    ],
    UserRoleEnum.MANAGER.value: [
        "assigned_city",
        "assigned_pincode",
        "assigned_area",
    ],
    UserRoleEnum.SUPERVISOR.value: [
        "assigned_city",
        "assigned_pincode",
        "assigned_area",
    ],
    UserRoleEnum.FIELD_OFFICER.value: [
        "assigned_city",
        "assigned_pincode",
        "assigned_area",
    ],
}


def parameter_key_validation(user_role: str, params: Dict) -> bool:
    """
    Validate query parameters against allowed filters for the user's role.

    Ensures:
    - A user cannot filter on region fields outside their permitted role scope.
    - If a filter requires parent filters, those must also be provided.

    Args:
        user_role (str): The role of the user (e.g., ADMIN, SR_MANAGER).
        params (Dict): Dictionary of query parameters from the request.

    Returns:
        bool: True if all parameters are valid, False otherwise.
    """
    user_access_fields: List[str] = USER_REGION_LEVEL_FIELD.get(user_role, [])

    # 1. Prevent access to disallowed region-level filters
    for param_key, value in params.items():
        if (
            param_key in REGION_FILTER_VALUES
            and value
            and param_key not in user_access_fields
        ):
            return False

    return True


def user_management_table_filter_queryset(
    queryset: QuerySet[UserModel], user_instance: UserModel, params: Dict
) -> QuerySet[UserModel]:
    """
    Apply filtering to the user management queryset based on role,
    status, and hierarchical region-level filters.

    Steps:
    1. Validate query parameters for role-based access.
    2. Limit queryset to users within the current user's reporting hierarchy.
    3. Apply filters on:
        - Status
        - User role
        - Region assignments (region, zone, city, pincode, area)

    Args:
        queryset (QuerySet[UserModel]): Base queryset of users.
        user_instance (UserModel): The requesting user.
        params (Dict): Request parameters for filtering.

    Returns:
        QuerySet[UserModel]: Filtered queryset.
    """
    # Extract query params (split by comma into lists)
    status: List[str] = (
        str(params.get("status", "")).split(",") if params.get("status") else []
    )
    user_role: List[str] = (
        str(params.get("user_role", "")).split(",") if params.get("user_role") else []
    )
    # Region-level filters
    region_filters: Dict[str, List[str]] = {}
    for field in REGION_FILTER_VALUES:
        if params.get(field):
            region_filters[field] = params.get(field)
            print(
                "RELATIONAL_FILTER_VALUES.get(field)",
                RELATIONAL_FILTER_VALUES.get(field),
            )
            if RELATIONAL_FILTER_VALUES.get(field):
                for related_fields in RELATIONAL_FILTER_VALUES[field]:
                    region_filters[related_fields] = params.get(field)

    # 1. Validate parameters against user role permissions
    if not parameter_key_validation(
        user_role=user_instance.user_role.role, params=params
    ):
        raise Exception("User tried to access unauthorized parameter(s) for this role")
    # 2. Restrict queryset to users under current user's reporting hierarchy
    queryset: QuerySet[UserModel] = get_user_reports_to_queryset(
        user_instance=user_instance,
        user_role=user_instance.user_role.pk,
        queryset=queryset,
    )

    # 3. Apply simple filters (status, role)
    filterset: Dict = {}
    if status:
        filterset["status__in"] = status
    if user_role:
        filterset["user_role__pk__in"] = user_role
    queryset: QuerySet[UserModel] = queryset.filter(**filterset)
    # 4. Build region-level filters using Q objects

    user_detail_filterset: Q = Q()
    for field, values in region_filters.items():

        if values:  # Apply only if this filter is provided
            print("values", values)
            user_detail_filterset |= Q(**{f"{field}__pk__in": str(values).split(",")})

    # 5. Filter UserDetailModel and link back to users
    user_detail_queryset: QuerySet[UserDetailModel] = UserDetailModel.objects.filter(
        user__pk__in=queryset.values_list("pk", flat=True)
    ).filter(user_detail_filterset)
    # Return only users matching filtered UserDetailModel
    return queryset.filter(
        pk__in=user_detail_queryset.values_list("user__pk", flat=True)
    )
