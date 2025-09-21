from typing import List, Optional
from user_config.user_auth.models import UserRoleModel


def get_descendant_roles(
    user_role_instance: UserRoleModel,
    role_hierarchy: Optional[List[UserRoleModel]] = None,
) -> List[UserRoleModel]:
    """
    Recursively retrieves all descendant roles (child roles under the given role).

    Args:
        user_role_instance (UserRoleModel):
            The role instance for which child roles need to be fetched.
        role_hierarchy (Optional[List[UserRoleModel]], default=None):
            Accumulator used to collect child roles during recursion.

    Returns:
        List[UserRoleModel]:
            A list of UserRoleModel instances representing all roles
            below the given role in the hierarchy.
    """
    # Initialize the accumulator list only once
    if role_hierarchy is None:
        role_hierarchy: List = []

    # Get the last child role (via reverse FK relation: reports_to → children)
    child: Optional[UserRoleModel] = (
        user_role_instance.UserRoleModel_reports_to.all().last()
    )

    # If a child exists, add it and recurse further down
    if child:
        role_hierarchy.append(child)
        return get_descendant_roles(child, role_hierarchy)

    # Base case: no children → return accumulated roles
    return role_hierarchy


def get_ancestor_roles(
    user_role_instance: UserRoleModel,
    role_hierarchy: Optional[List[UserRoleModel]] = None,
) -> List[UserRoleModel]:
    """
    Recursively retrieves all ancestor roles (parent roles above the given role).

    Args:
        user_role_instance (UserRoleModel):
            The role instance for which ancestor roles need to be fetched.
        role_hierarchy (Optional[List[UserRoleModel]], default=None):
            Accumulator used to collect parent roles during recursion.

    Returns:
        List[UserRoleModel]:
            A list of UserRoleModel instances representing all roles
            above the given role in the hierarchy.
    """
    # Initialize the accumulator list only once
    if role_hierarchy is None:
        role_hierarchy: List = []

    # Get the immediate parent role
    parent: Optional[UserRoleModel] = user_role_instance.reports_to

    # If a parent exists, add it and recurse further up
    if parent:
        role_hierarchy.append(parent)
        return get_ancestor_roles(parent, role_hierarchy)

    # Base case: no parent → return accumulated roles
    return role_hierarchy
