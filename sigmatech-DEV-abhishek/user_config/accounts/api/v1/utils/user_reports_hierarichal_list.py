from core_utils.utils.global_variables import (
    STATUS_ACTIVATED_GLOBAL_FILTERSET,
    USER_MODEL_EXCLUDE_ADMIN_ROLE_FILTERSET,
)
from user_config.user_auth.enums import UserRoleEnum
from user_config.user_auth.models import UserModel
from typing import List, Optional


def get_ancestor_users(
    user_instance: UserModel,
    user_hierarchy: Optional[List[UserModel]] = None,
) -> List[UserModel]:
    """
    Recursively retrieves all ancestor users (managers, supervisors, etc.)
    above the given user instance in the reporting hierarchy.

    Args:
        user_instance (UserModel):
            The user instance whose ancestors need to be fetched.
        user_hierarchy (Optional[List[UserModel]], default=None):
            Accumulator used to collect ancestor users during recursion.

    Returns:
        List[UserModel]:
            A list of UserModel instances representing all users above
            the given user in the reporting hierarchy.
    """
    # Initialize accumulator only once
    if user_hierarchy is None:
        user_hierarchy: List = []

    # Get the immediate manager/supervisor of the user
    parent: Optional[UserModel] = user_instance.reports_to

    # If a manager exists, add to the hierarchy and recurse further up
    if parent:
        user_hierarchy.append(parent)
        return get_ancestor_users(parent, user_hierarchy)

    # Base case: no more parents → return accumulated hierarchy
    return user_hierarchy


def get_descendant_users(
    user_instance: UserModel,
    user_hierarchy: Optional[List[UserModel]] = None,
) -> List[UserModel]:
    """
    Recursively retrieves all descendant users (direct and indirect reports)
    under the given user instance.

    Args:
        user_instance (UserModel):
            The user instance whose subordinates need to be fetched.
        user_hierarchy (Optional[List[UserModel]], default=None):
            Accumulator used to collect subordinate users during recursion.

    Returns:
        List[UserModel]:
            A list of UserModel instances representing all users under
            the given user in the reporting hierarchy.
    """
    # Initialize accumulator only once
    if user_instance.user_role.role == UserRoleEnum.ADMIN.value:
        return list(
            UserModel.objects.filter(**STATUS_ACTIVATED_GLOBAL_FILTERSET).exclude(
                **USER_MODEL_EXCLUDE_ADMIN_ROLE_FILTERSET
            )
        )
    if user_hierarchy is None:
        user_hierarchy: List = []

    # Get all direct reports of the current user
    children: List[UserModel] = list(user_instance.UserModel_reports_to.all())

    # If there are direct reports, collect them and recurse for each
    for child in children:
        user_hierarchy.append(child)
        get_descendant_users(child, user_hierarchy)

    # Base case: no more children → return accumulated hierarchy
    return user_hierarchy
