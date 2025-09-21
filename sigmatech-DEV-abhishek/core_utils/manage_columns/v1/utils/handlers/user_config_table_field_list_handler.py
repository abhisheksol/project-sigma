from core_utils.manage_columns.models import (
    CoreUtilsFeaturesModel,
    UserConfigTableOrderModel,
)
from core_utils.manage_columns.v1.utils.handlers.constants import (
    FEATURE_TITLE_REQUIRED_ERROR_MESSAGE,
    INCORRECT_FEATURE_ERROR_MESSAGE,
)
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from core_utils.utils.string_to_class import get_keys_of_serializer
from typing import List, Optional


class UserConfigTableFieldListHandler(CoreGenericBaseHandler):
    """
    Handler for managing user-configured table fields (active/inactive columns)
    for a given feature.

    Responsibilities:
    - Validate the `feature_title` passed in request data.
    - Fetch the user's saved column preferences (if any).
    - If no preferences exist, initialize defaults from the feature serializer.
    - Prepare active/inactive field lists.
    - Build the final response containing field status and pagination size.
    """

    # Querysets for features and user preferences
    feature_queryset = CoreUtilsFeaturesModel.objects.all()
    feature_user_preference_queryset = UserConfigTableOrderModel.objects.all()

    # Instance of user preferences for the current feature (if found)
    feature_user_preference_instance: Optional[UserConfigTableOrderModel] = None

    # Lists to hold active/inactive field titles
    active_titles: List[str]
    inactive_titles: List[str]

    def validate(self):
        """
        Validate and prepare active/inactive fields for a given feature.

        Steps:
        1. Check that `table__feature__title` is provided in the request.
        2. Verify that the feature exists in the database.
        3. Check if the user already has preferences saved for the feature.
        4. Populate `active_titles` and `inactive_titles` from preferences,
           or fall back to the feature serializer fields.
        """

        # Step 1: Validate feature title
        feature_title = self.data.get("table__feature__title")
        if not feature_title:
            return self.set_error_message(
                FEATURE_TITLE_REQUIRED_ERROR_MESSAGE, key="table__feature__title"
            )

        # Step 2: Check if feature exists
        if not self.feature_queryset.filter(title=feature_title).exists():
            return self.set_error_message(
                INCORRECT_FEATURE_ERROR_MESSAGE, key="table__feature__title"
            )

        # Fetch the feature instance
        feature_instance = self.feature_queryset.get(title=feature_title)

        # Step 3: Check if user has saved preferences for this feature
        if self.feature_user_preference_queryset.filter(
            feature=feature_instance, user=self.request.user
        ).exists():
            self.feature_user_preference_instance = (
                UserConfigTableOrderModel.objects.get(
                    feature=feature_instance, user=self.request.user
                )
            )

        # Step 4: Build queryset for user-specific table fields
        self.queryset = self.queryset.filter(
            table__user=self.request.user, table__feature=feature_instance
        ).order_by("order")

        # Populate active/inactive titles
        if self.queryset.exists():
            # From existing user configuration
            self.active_titles = [
                i["title"] for i in self.queryset.filter(is_active=True).values("title")
            ]
            self.inactive_titles = [
                i["title"]
                for i in self.queryset.filter(is_active=False).values("title")
            ]
        else:
            # Default from serializer if no saved preferences
            self.active_titles = get_keys_of_serializer(feature_instance.serializer)
            self.inactive_titles = []

    def create(self):
        """
        Build the final response structure containing:
        - Field activation status (active/inactive).
        - Pagination size (from user preferences, defaults to 10).
        """

        # Build a dictionary of fields and their active status
        field_data: dict = {}
        for data in [*self.active_titles, *self.inactive_titles]:
            field_data[data] = data in self.active_titles

        # Prepare response data
        self.data["results"] = {
            "field_data": field_data,
            "pagination_size": (
                self.feature_user_preference_instance.pagination_size
                if self.feature_user_preference_instance
                else 10
            ),
        }
