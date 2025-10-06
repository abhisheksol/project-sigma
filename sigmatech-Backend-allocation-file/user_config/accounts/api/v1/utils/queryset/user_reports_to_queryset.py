from typing import Dict, List
from django.db.models.query import QuerySet

from user_config.user_auth.models import UserModel, UserRoleModel
from user_config.user_auth.enums import UserRoleEnum
from user_config.accounts.api.v1.utils.user_reports_hierarichal_list import (
    get_descendant_users,
)


def get_user_reports_queryset(
    queryset: QuerySet[UserModel], params: Dict, request_user: UserModel
) -> QuerySet[UserModel]:
    """
    Filters UserModel queryset based on 'reports_to', 'reports_to_user_role',
    or 'user_role' query parameters.

    Args:
        queryset (QuerySet[UserModel]): Base queryset of UserModel.
        params (Dict): Query parameters from request.GET.
        request_user (UserModel): The currently authenticated user.

    Returns:
        QuerySet[UserModel]: A filtered queryset of users based on reporting hierarchy and region/zone/city.
    """

    if params.get("reports_to"):
        # Filter directly by reports_to field
        return queryset.filter(reports_to__pk=params["reports_to"])

    elif params.get("reports_to_user_role"):
        # Get user instance based on the role parameter
        user_instance: UserModel = queryset.get(pk=params["reports_to_user_role"])
        filterset: Dict = {}

        # If user is not Admin/SR Manager, restrict to their role
        if user_instance.user_role.role not in [
            UserRoleEnum.ADMIN.value,
            UserRoleEnum.SR_MANAGER.value,
        ]:
            filterset["user_role__pk"] = user_instance.user_role.pk
            reports_to_user: UserModel = user_instance.reports_to
        else:
            reports_to_user: UserModel = request_user

        # Base queryset for descendants
        descendant_queryset = get_user_reports_to_queryset(
            queryset=queryset,
            user_role=user_instance.user_role.pk,
            user_instance=reports_to_user,
        ).exclude(pk=user_instance.pk)

        # Filter based on role and assigned region/zone/city
        if user_instance.user_role.role == UserRoleEnum.SR_MANAGER.value:
            # Get regions assigned to the user_instance
            assigned_regions = user_instance.UserDetailModel_user.assigned_region.all()
            return descendant_queryset.filter(
                user_role__pk=user_instance.user_role.pk,
                UserDetailModel_user__assigned_region__in=assigned_regions,
            )
        elif user_instance.user_role.role == UserRoleEnum.MANAGER.value:
            # Get zones assigned to the user_instance
            assigned_zones = user_instance.UserDetailModel_user.assigned_zone.all()
            return descendant_queryset.filter(
                user_role__pk=user_instance.user_role.pk,
                UserDetailModel_user__assigned_zone__in=assigned_zones,
            )
        elif user_instance.user_role.role == UserRoleEnum.SUPERVISOR.value:
            # Get cities assigned to the user_instance
            assigned_cities = user_instance.UserDetailModel_user.assigned_city.all()
            return descendant_queryset.filter(
                user_role__pk=user_instance.user_role.pk,
                UserDetailModel_user__assigned_city__in=assigned_cities,
            )
        else:
            # For other roles (e.g., FIELD_OFFICER or ADMIN), apply role filter only
            return descendant_queryset.filter(**filterset)

    elif params.get("user_role"):
        # Filter by role and hierarchy
        return get_user_reports_to_queryset(
            queryset=queryset,
            user_role=UserRoleModel.objects.get(pk=params["user_role"]).reports_to.pk,
            user_instance=request_user,
            include_current_user=True,
        ).filter(
            user_role=UserRoleModel.objects.get(pk=params["user_role"]).reports_to,
        )

    # Default: return empty set
    return queryset.none()


def get_user_reports_to_queryset(
    queryset: QuerySet[UserModel],
    user_role: str,
    user_instance: UserModel,
    include_current_user: bool = False,
) -> QuerySet[UserModel]:
    """
    Filters a queryset of UserModel to include only users who are:
      1. Descendants (direct or indirect reports) of the given user_instance
      2. Assigned to a specific user_role.

    Args:
        queryset (QuerySet[UserModel]):
            The base queryset of UserModel to filter.
        user_role (str):
            The role ID/PK used to filter users by role.
        user_instance (UserModel):
            The user instance whose reporting hierarchy will be considered.

    Returns:
        QuerySet[UserModel]:
            A filtered queryset containing users who:
              - Report (directly or indirectly) to the given user_instance
              - Belong to the specified user_role
              - Excludes admin users unless the requesting user is an admin
    """

    # Get the role instance for filtering
    user_role_instance: UserRoleModel = UserRoleModel.objects.get(pk=user_role)

    # If the requesting user is an Admin, return all users except Admins
    if user_role_instance.role in [UserRoleEnum.ADMIN.value]:
        return queryset.exclude(user_role__role=UserRoleEnum.ADMIN.value)

    # Get all descendant users (direct & indirect reports)
    descendant_users_list: List[UserModel] = get_descendant_users(
        user_instance=user_instance
    )
    include_current_user_list: List[str] = []
    if include_current_user:
        include_current_user_list: List[str] = [user_instance.pk]

    return queryset.filter(
        pk__in=[
            *[query.pk for query in descendant_users_list],
            *include_current_user_list,
        ]
    )
