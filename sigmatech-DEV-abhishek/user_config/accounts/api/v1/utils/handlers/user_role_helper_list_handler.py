from typing import List, Dict, Any
from core_utils.utils.convert_utils import get_values_from_list_of_queryset
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from user_config.accounts.api.v1.utils.user_role_hierarichal_list import (
    get_descendant_roles,
)
from user_config.user_auth.models import UserRoleModel


class UserRoleHelperListHanlder(CoreGenericBaseHandler):
    """
    Handler class for retrieving and serializing descendant user roles
    of the currently authenticated user's role.
    """

    # Stores the serialized results of user role hierarchy
    results: List[Dict[str, Any]]

    def validate(self) -> None:
        """
        Validates and prepares data by fetching all descendant roles
        for the current user's role and converting them into a list
        of dictionaries with selected fields.

        This method sets the `results` attribute for later use in `create()`.
        """
        # Get all descendant roles of the logged-in user's role
        role_queryset: List[UserRoleModel] = get_descendant_roles(
            user_role_instance=self.request.user.user_role
        )

        # Extract only required fields (`id`, `title`) from the queryset
        result: List[Dict] = get_values_from_list_of_queryset(
            queryset=role_queryset, values_list=["id", "title", "icons", "role"]
        )
        modified_result: List[Dict] = []

        for item in result:
            modified_item: Dict = {
                "value": item["id"],
                "label": item["title"],
                "icons": item["icons"],
                "role": item["role"],
            }
            modified_result.append(modified_item)
        self.results: List[Dict] = modified_result

    def create(self) -> None:
        """
        Populates the response data with the prepared results.

        This method assumes that `validate()` has already been called,
        so `self.results` contains the processed user role hierarchy.
        """
        # Assign results into the handler's data dictionary for serializer
        self.data["results"] = self.results
