"""
User Management Filtering Utilities

This module provides utility functions to validate query parameters and
filter user querysets based on role-based permissions, hierarchical
reporting, and region-level assignments (region, zone, city, pincode, area).
"""

from typing import Dict, List
from django.db.models.query import QuerySet
import uuid
from core_utils.utils.global_variables import STATUS_ACTIVATED_GLOBAL_FILTERSET
from user_config.user_auth.models import UserModel
from user_config.accounts.models import UserAssignedProdudctsModel, UserDetailModel
from user_config.user_auth.enums import UserRoleEnum
from user_config.accounts.api.v1.utils.queryset.user_reports_to_queryset import (
    get_user_reports_to_queryset,
)
from django.db.models import QuerySet, CharField, Value, Prefetch, F
from django.db.models.functions import Concat

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
    Applies comprehensive filtering to a user management queryset based on role, status, and hierarchical region assignments.

    This function processes a queryset of UserModel instances, applying filters based on:
    - The requesting user's role and permissions to ensure authorized access.
    - The reporting hierarchy to limit results to users under the requesting user's supervision.
    - Query parameters for status, user role, and region-level assignments (region, zone, city, pincode, area).
    - Product assignment IDs for additional filtering.

    Steps:
    1. Extract and validate query parameters (status, user_role, region-level filters).
    2. Restrict the queryset to users within the requesting user's reporting hierarchy.
    3. Apply simple filters for status and user role.
    4. Apply product assignment filters if provided.
    5. Apply region-level filters using a custom UserDetailQuerySet for hierarchical region assignments, with multiple regions/zones combined using OR logic.
    6. Optimize the queryset with prefetching for product assignments and annotate assignment names.
    7. Return the filtered queryset, ensuring only users matching the UserDetailModel filters are included.

    Args:
        queryset (QuerySet[UserModel]): The initial queryset of UserModel instances to filter.
        user_instance (UserModel): The requesting user, used to enforce role-based permissions and hierarchy.
        params (Dict): Dictionary of query parameters for filtering (e.g., status, user_role, region assignments).

    Returns:
        QuerySet[UserModel]: A filtered queryset of users matching the specified criteria.

    Raises:
        Exception: If the requesting user attempts to access unauthorized parameters for their role.
    """
    # Extract query params (split by comma into lists)
    status: List[str] = (
        str(params.get("status", "")).split(",") if params.get("status") else []
    )
    user_role: List[str] = (
        str(params.get("user_role", "")).split(",") if params.get("user_role") else []
    )
    # Extract region-level filters from query parameters
    region_filters: Dict[str, List[str]] = {}
    for field in REGION_FILTER_VALUES:
        if params.get(field):
            region_filters[field] = params.get(field)
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

    # 3. Apply simple filters for status and role
    filterset: Dict = {}
    if status:
        filterset["status__in"] = status
    if user_role:
        filterset["user_role__pk__in"] = user_role
    queryset: QuerySet[UserModel] = queryset.filter(**filterset)

    # 3.1 Extract product_assignment_id from query params
    product_assignment_ids: List[uuid.UUID] = [
        uuid.UUID(pid)
        for pid in str(params.get("product_assignment_id", "")).split(",")
        if pid
    ]

    # 3.2 Apply filter if provided
    if product_assignment_ids:
        queryset = queryset.filter(
            UserAssignedProdudctsModel_user__product_assignment__id__in=product_assignment_ids
        ).distinct()

    # 4. Build region-level filters using Q objects
    assigned_region: List[str] = (
        str(params.get("assigned_region", "")).split(",")
        if params.get("assigned_region")
        else []
    )
    assigned_zone: List[str] = (
        str(params.get("assigned_zone", "")).split(",")
        if params.get("assigned_zone")
        else []
    )

    user_detail_queryset: QuerySet[UserDetailModel] = UserDetailModel.objects.all()

    # Apply region filter if provided (OR logic for multiple regions)
    if assigned_region:
        user_detail_queryset: QuerySet[UserDetailModel] = (
            user_detail_queryset.filter_by_region(assigned_region)
        )

    # Apply zone filter if provided (OR logic for multiple zones, AND with other filters)
    if assigned_zone:
        user_detail_queryset: QuerySet[UserDetailModel] = (
            user_detail_queryset.filter_by_zone(assigned_zone)
        )

    # Apply direct region filters (city, pincode, area) if provided (AND logic)
    direct_region_filters: List[str] = [
        "assigned_city",
        "assigned_pincode",
        "assigned_area",
    ]
    for region_filter in direct_region_filters:
        if params.get(region_filter):
            user_detail_queryset: QuerySet[UserDetailModel] = (
                user_detail_queryset.filter(
                    **{
                        f"{region_filter}__pk__in": str(params[region_filter]).split(
                            ","
                        )
                    }
                )
            )

    # Optimize queryset by prefetching related product assignments and annotating assignment names
    queryset = queryset.prefetch_related(
        Prefetch(
            "UserAssignedProdudctsModel_user",  # Relation from User to UserAssignedProdudctsModel
            queryset=UserAssignedProdudctsModel.objects.filter(
                **STATUS_ACTIVATED_GLOBAL_FILTERSET
            ).annotate(
                assignment=Concat(
                    F("product_assignment__process__title"),
                    Value("-"),
                    F("product_assignment__product__title"),
                    output_field=CharField(),
                )
            ),
            to_attr="product_assignment_name",  # Stores annotated objects as a list
        )
    )

    # Return only users matching the filtered UserDetailModel instances
    return queryset.filter(
        pk__in=user_detail_queryset.values_list("user__pk", flat=True)
    )
