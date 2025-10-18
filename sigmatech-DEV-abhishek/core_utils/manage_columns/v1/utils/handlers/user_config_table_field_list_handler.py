from core_utils.manage_columns.models import (
    CoreUtilsFeaturesModel,
    UserConfigTableOrderModel,
)
from core_utils.manage_columns.v1.utils.handlers.constants import (
    FEATURE_TITLE_REQUIRED_ERROR_MESSAGE,
    INCORRECT_FEATURE_ERROR_MESSAGE,
)
from core_utils.manage_columns.v1.utils.manage_column import (
    create_or_update_table_column_fields,
)
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from core_utils.utils.string_to_class import (
    get_keys_of_serializer,
    string_to_serializer,
)
from typing import List, Optional
from rest_framework.serializers import Serializer


class UserConfigTableFieldListHandler(CoreGenericBaseHandler):
    """
    Manages user-configured table fields for a specified feature, handling active and inactive columns.

    This class validates the provided feature title, retrieves or initializes user preferences for table fields,
    and constructs a response with active/inactive field statuses and pagination settings. It ensures that
    user-specific column configurations are fetched from the database or initialized from the feature's serializer
    if no preferences exist. The handler supports dynamic table customization for a given user and feature.

    Attributes:
        feature_queryset: QuerySet for CoreUtilsFeaturesModel to fetch feature details.
        feature_user_preference_queryset: QuerySet for UserConfigTableOrderModel to fetch user preferences.
        feature_user_preference_instance (Optional[UserConfigTableOrderModel]): User preferences for the feature, if found.
        active_titles (List[str]): List of field titles marked as active for the user.
        inactive_titles (List[str]): List of field titles marked as inactive for the user.
    """

    # Querysets for accessing feature and user preference data
    feature_queryset = CoreUtilsFeaturesModel.objects.all()
    feature_user_preference_queryset = UserConfigTableOrderModel.objects.all()

    # Instance to store user preferences for the current feature, if available
    feature_user_preference_instance: Optional[UserConfigTableOrderModel] = None

    # Lists to store titles of active and inactive fields
    active_titles: List[str]
    inactive_titles: List[str]

    def validate(self) -> None:
        """
        Validates the input feature title and prepares active/inactive field lists.

        Performs the following steps:
        1. Ensures the `table__feature__title` is provided in the request data.
        2. Verifies that the specified feature exists in the database.
        3. Checks for existing user preferences for the feature.
        4. Populates `active_titles` and `inactive_titles` based on user preferences or defaults to serializer fields.
        5. If no preferences exist, initializes them using the feature's serializer and default column settings.

        Side Effects:
            - Sets `self.feature_user_preference_instance` if user preferences are found.
            - Updates `self.queryset` to filter user-specific table fields.
            - Populates `self.active_titles` and `self.inactive_titles` with field titles.
            - Calls `create_or_update_table_column_fields` to initialize preferences if none exist.
            - Sets error messages via `self.set_error_message` if validation fails.
        """
        # Step 1: Validate the presence of feature title in request data
        feature_title: Optional[str] = self.data.get("table__feature__title")
        print("feature_title", feature_title)
        if not feature_title:
            return self.set_error_message(
                FEATURE_TITLE_REQUIRED_ERROR_MESSAGE, key="table__feature__title"
            )

        # Step 2: Verify the feature exists in the database
        if not self.feature_queryset.filter(title=feature_title).exists():
            return self.set_error_message(
                INCORRECT_FEATURE_ERROR_MESSAGE, key="table__feature__title"
            )

        # Fetch the feature instance for the given title
        feature_instance: CoreUtilsFeaturesModel = self.feature_queryset.get(
            title=feature_title
        )

        # Step 3: Check for existing user preferences for the feature
        if self.feature_user_preference_queryset.filter(
            feature=feature_instance, user=self.request.user
        ).exists():
            self.feature_user_preference_instance = (
                UserConfigTableOrderModel.objects.get(
                    feature=feature_instance, user=self.request.user
                )
            )

        # Step 4: Filter queryset for user-specific table fields, ordered by preference
        self.queryset = self.queryset.filter(
            table__user=self.request.user, table__feature=feature_instance
        ).order_by("order")

        # Step 5: Populate active and inactive field titles
        if self.queryset.exists():
            # Retrieve active and inactive titles from existing user configuration
            self.active_titles = [
                i["title"] for i in self.queryset.filter(is_active=True).values("title")
            ]
            self.inactive_titles = [
                i["title"]
                for i in self.queryset.filter(is_active=False).values("title")
            ]
        else:
            # Initialize with default fields from the feature's serializer
            self.active_titles = get_keys_of_serializer(feature_instance.serializer)
            self.inactive_titles = []

            # Create serializer instance to access default column fields
            serializer_instance: Serializer = string_to_serializer(
                serializer_string=feature_instance.serializer
            )
            default_manage_column_fields: List[str] = getattr(
                serializer_instance, "default_manage_column_fields", []
            )
            # Determine inactive fields (those not in default_manage_column_fields)
            inactive_fields: List[str] = [
                i for i in self.active_titles if i not in default_manage_column_fields
            ]
            if default_manage_column_fields:
                # Initialize user preferences with default active/inactive fields
                create_or_update_table_column_fields(
                    feature_instance=feature_instance,
                    active_title=default_manage_column_fields,
                    in_active_title=inactive_fields,
                    user_instance=self.request.user,
                )
                # Re-fetch active/inactive titles after initialization
                self.active_titles = [
                    i["title"]
                    for i in self.queryset.filter(is_active=True).values("title")
                ]
                self.inactive_titles = [
                    i["title"]
                    for i in self.queryset.filter(is_active=False).values("title")
                ]

    def create(self) -> None:
        """
        Constructs the response structure with field activation status and pagination size.

        Builds a dictionary mapping field titles to their active/inactive status and includes
        the pagination size from user preferences (or defaults to 10). The response is stored
        in `self.data["results"]` for further processing by the API view.

        Side Effects:
            - Modifies `self.data["results"]` to include:
                - `field_data`: Dictionary mapping field titles to their active status (True/False).
                - `pagination_size`: Integer representing the user's preferred pagination size or default (10).
        """
        # Initialize dictionary to store field activation status
        field_data: dict = {}
        # Combine active and inactive titles, marking active status
        for data in [*self.active_titles, *self.inactive_titles]:
            field_data[data] = data in self.active_titles

        # Construct response with field data and pagination size
        self.data["results"] = {
            "field_data": field_data,
            "pagination_size": (
                self.feature_user_preference_instance.pagination_size
                if self.feature_user_preference_instance
                else 10
            ),
        }
