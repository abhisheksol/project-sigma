from user_config.accounts.api.v1.utils.user_role_hierarichal_list import (
    get_descendant_roles,
)
from user_config.user_auth.models import UserModel, UserRoleModel
from typing import List, Any
from user_config.accounts.api.v1.utils.user_reports_hierarichal_list import (
    get_descendant_users,
)


def list_of_has_permission_roles(user_role_instance: UserRoleModel, key: str = "pk"):
    descendant_roles_queryset_list: List[UserRoleModel] = get_descendant_roles(
        user_role_instance=user_role_instance
    )
    descendant_roles_list: List[Any] = [
        str(getattr(query, key)) for query in descendant_roles_queryset_list
    ]
    return descendant_roles_list


def list_of_user_id_under_user_instance(
    user_instance: UserModel, key: str = "pk", include_current_user: bool = True
) -> List[str]:
    user_queryset_list: List[UserModel] = get_descendant_users(
        user_instance=user_instance
    )
    if include_current_user:
        return [
            *[str(getattr(query, key)) for query in user_queryset_list],
            str(getattr(user_instance, key)),
        ]
    return [str(getattr(query, key)) for query in user_queryset_list]


def has_user_permission_to_role(
    user_instance: UserModel, user_role_instance: UserRoleModel
) -> bool:

    return [
        str(user_role_instance.pk)
        in list_of_has_permission_roles(
            user_role_instance=user_instance.user_role, key="pk"
        )
    ]
