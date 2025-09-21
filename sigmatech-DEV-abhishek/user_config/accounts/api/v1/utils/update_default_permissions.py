from typing import List, Dict
from django.db.models.query import QuerySet
from django.db import transaction

from user_config.accounts.api.v1.utils.default_permissions import (
    DEFAULT_PERMISSIONS_TO_USER_ROLE,
)
from user_config.user_auth.models import UserModel
from user_config.permissions.models import (
    UserConfigPermissionsModel,
    UserConfigUserAssignedPermissionsModel,
)


def _assign_permission_if_missing(
    user: UserModel,
    permission_obj: UserConfigPermissionsModel,
    read_only: bool = False,
    all_access: bool = False,
) -> None:
    """
    Helper function to assign a permission to a user only if not already assigned.

    Args:
        user (UserModel): Target user instance.
        permission_obj (UserConfigPermissionsModel): The permission object.
        read_only (bool): Flag to assign with read-only access.
        all_access (bool): Flag to assign with full access.
    """
    already_assigned = UserConfigUserAssignedPermissionsModel.objects.filter(
        user=user, permission=permission_obj
    ).exists()

    if not already_assigned:
        UserConfigUserAssignedPermissionsModel.objects.create(
            permission=permission_obj,
            user=user,
            read_only_access=read_only,
            all_access=all_access,
        )


def set_default_user_permissions(user_instance: UserModel) -> None:
    """
    Assigns default permissions to a newly created user based on their role.

    - Each role in the system (Manager, Supervisor, Field Officer, etc.)
      has a predefined set of default permissions defined in
      `DEFAULT_PERMISSIONS_TO_USER_ROLE`.
    - Only permissions marked with `"has_access": True` will be assigned.
    - Ensures duplicate entries are not created by checking first.

    Args:
        user_instance (UserModel): The user instance for which to assign default permissions.

    Returns:
        None
    """

    # Fetch the default permission structure for this user's role
    default_permissions: List[Dict] = DEFAULT_PERMISSIONS_TO_USER_ROLE.get(
        user_instance.user_role.role, []
    )

    # Only fetch sub-permissions (child permissions, not top-level)
    permission_queryset: QuerySet[UserConfigPermissionsModel] = (
        UserConfigPermissionsModel.objects.filter(parent_permission__isnull=False)
    )

    with transaction.atomic():
        for permission_group in default_permissions:
            sub_permissions: List = permission_group.get("sub_permissions", [])

            for permission in sub_permissions:
                if permission.get("has_access"):
                    # Lookup the permission object
                    permission_obj = permission_queryset.filter(
                        pk=permission["id"]
                    ).first()
                    if not permission_obj:
                        continue  # Skip missing permissions (edge case)

                    # Assign with default access (not read-only, not all-access)
                    _assign_permission_if_missing(
                        user=user_instance,
                        permission_obj=permission_obj,
                        read_only=False,
                        all_access=False,
                    )


def assign_default_all_permissions(user_instance: UserModel) -> None:
    """
    Assigns **all permissions** in the system to the given user.

    - Clears all existing user-permission mappings.
    - Assigns every child permission (ignores parent-level permissions).
    - Marks each assigned permission with `read_only_access=True`
      and `all_access=True`.

    Args:
        user_instance (UserModel): The user instance to assign permissions for.

    Returns:
        None
    """

    # Only fetch sub-permissions (child permissions)
    permission_queryset: QuerySet[UserConfigPermissionsModel] = (
        UserConfigPermissionsModel.objects.filter(parent_permission__isnull=False)
    )

    # Remove existing user assignments
    user_assigned_queryset: QuerySet[UserConfigUserAssignedPermissionsModel] = (
        UserConfigUserAssignedPermissionsModel.objects.filter(user=user_instance)
    )

    with transaction.atomic():
        user_assigned_queryset.delete()

        for permission_obj in permission_queryset:
            _assign_permission_if_missing(
                user=user_instance,
                permission_obj=permission_obj,
                read_only=True,
                all_access=True,
            )
