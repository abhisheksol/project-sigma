from typing import List, Dict
from django.db.models.query import QuerySet
from user_config.permissions.models import (
    UserConfigPermissionsModel,
    UserConfigUserAssignedPermissionsModel,
)
from user_config.user_auth.models import UserModel
from user_config.user_auth.enums import UserRoleEnum


def get_permissions_and_user_access(
    permission_instance: UserConfigPermissionsModel,
    user_instance: UserModel,
    is_login_user: bool,
) -> List[Dict[str, bool]]:
    """
    Fetch child permissions under a given permission and mark whether
    the given user has access to them (including read_only_access, all_access).
    """
    # Get all child permissions of the given parent
    permission_queryset: QuerySet[UserConfigPermissionsModel] = (
        UserConfigPermissionsModel.objects.filter(parent_permission=permission_instance)
    )

    # Fetch user assigned permissions (id → flags)
    user_permissions_map: Dict = {
        str(upa.permission_id): {
            "read_only_access": upa.read_only_access,
            "all_access": upa.all_access,
        }
        for upa in UserConfigUserAssignedPermissionsModel.objects.filter(
            user=user_instance
        )
    }

    # Build the response
    permissions_with_access: List[Dict[str, bool]] = []
    for perm in permission_queryset:
        if user_instance.user_role.role == UserRoleEnum.ADMIN.value:
            # Admin have all the permissions
            access_data: Dict = {
                "read_only_access": True,
                "all_access": True,
            }
        elif str(perm.id) in user_permissions_map:
            # User has this permission → include access flags
            access_data: Dict = user_permissions_map[str(perm.id)]
        else:
            # User does not have this permission
            access_data: Dict = {
                "read_only_access": False,
                "all_access": False,
            }
        if is_login_user:
            permissions_with_access.extend(
                [
                    {
                        "id": str(perm.id),
                        "title": f"{perm.title} view",
                        "has_access": access_data["read_only_access"],
                    },
                    {
                        "id": str(perm.id),
                        "title": f"{perm.title} edit",
                        "has_access": access_data["all_access"],
                    },
                ]
            )
        else:
            permissions_with_access.append(
                {
                    "id": str(perm.id),
                    "title": perm.title,
                    **access_data,
                }
            )

    return permissions_with_access
