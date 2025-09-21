from core_utils.manage_columns.v1.utils.handlers.constants import (
    FEATURE_TITLE_REQUIRED_ERROR_MESSAGE,
    INCORRECT_FEATURE_ERROR_MESSAGE,
    REQUIRED_FIELDS_ERROR_MESSAGE,
    ROW_COUNT_ERROR_MESSAGE,
    ROW_COUNT_REQUIRED_ERROR_MESSAGE,
)
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from core_utils.utils.string_to_class import get_keys_of_serializer
from core_utils.manage_columns.models import (
    CoreUtilsFeaturesModel,
    UserConfigTableFieldsModel,
    UserConfigTableOrderModel,
)
from core_utils.manage_columns.v1.utils.manage_column import (
    create_or_update_table_column_fields,
)
from typing import List
from user_config.user_auth.models import UserModel
from django.db.models.query import QuerySet
import logging


class UserConfigManageColumnHandler(CoreGenericBaseHandler):
    """
    Handler to manage and validate user table column preferences.

    Responsibilities:
    - Validate the request data (feature existence, pagination size, field lists).
    - Ensure active and inactive fields match the serializer definition.
    - Prevent common mistakes such as duplicate fields between active/inactive sets.
    - Persist user preferences using `create_or_update_table_column_fields`.
    """

    # Queryset to fetch available features
    feature_queryset: QuerySet[CoreUtilsFeaturesModel] = (
        CoreUtilsFeaturesModel.objects.all()
    )

    # Lists to store active and inactive field titles during validation
    active_title: List[str] = []
    in_active_title: List[str] = []

    # Logger for debugging
    logger = logging.getLogger(__name__)

    def validate(self):
        """
        Validate user-provided column configuration.

        Steps:
        1. Extract active and inactive fields from `results`.
        2. Ensure no field is present in both active and inactive lists.
        3. Ensure a valid `feature` is provided and exists in DB.
        4. Validate pagination rules (required and within range).
        5. Fetch serializer keys for the feature to compare against request.
        6. Ensure payload fields exactly match serializer-defined fields.

        Returns:
            dict: Cleaned and validated data.
        """
        self.logger.debug(f"Input data: {self.data}")
        self.data["feature"] = self.request.GET.dict().get("feature")

        # Step 1: Extract active/inactive fields from "results" dict
        self.active_title: List = []
        self.in_active_title: List = []
        for key in self.data["results"].keys():
            if self.data["results"][key]:
                self.active_title.append(key)
            else:
                self.in_active_title.append(key)

        self.logger.debug(f"Active titles: {self.active_title}")
        self.logger.debug(f"Inactive titles: {self.in_active_title}")

        # Step 2: Check for duplicates between active and inactive fields
        common_fields: set = set(self.active_title) & set(self.in_active_title)
        if common_fields:
            self.logger.error(f"Duplicate fields found: {common_fields}")
            return self.set_error_message(
                f"Fields cannot be both active and inactive: {common_fields}",
                key="results",
            )

        # Step 3: Validate feature presence
        if not self.data.get("feature"):
            self.logger.error("Feature not provided")
            return self.set_error_message(
                FEATURE_TITLE_REQUIRED_ERROR_MESSAGE, key="feature"
            )

        # Ensure feature exists in DB
        if not self.feature_queryset.filter(title=self.data["feature"]).exists():
            self.logger.error(f"Feature not found: {self.data['feature']}")
            return self.set_error_message(
                INCORRECT_FEATURE_ERROR_MESSAGE, key="feature"
            )

        # Get feature instance
        feature_instance = self.feature_queryset.get(title=self.data["feature"])
        self.logger.debug(f"Feature instance: {feature_instance.title}")

        # Step 4: Validate pagination count
        if not self.data.get("pagination_count"):
            self.logger.error("Pagination count not provided")
            return self.set_error_message(
                ROW_COUNT_REQUIRED_ERROR_MESSAGE, key="pagination_count"
            )

        if self.data["pagination_count"] < 5 or self.data["pagination_count"] > 250:
            self.logger.error(
                f"Invalid pagination count: {self.data['pagination_count']}"
            )
            return self.set_error_message(
                ROW_COUNT_ERROR_MESSAGE, key="pagination_count"
            )

        # Step 5: Get serializer-defined keys
        serializer_keys: List[str] = get_keys_of_serializer(feature_instance.serializer)
        self.logger.debug(
            f"Serializer keys for {self.data['feature']}: {serializer_keys}"
        )

        # Step 6: Ensure all serializer fields are accounted for
        if set(self.active_title + self.in_active_title) != set(serializer_keys):
            self.logger.error(
                f"Field mismatch. Provided: {set(self.active_title + self.in_active_title)}, Expected: {set(serializer_keys)}"
            )
            return self.set_error_message(
                REQUIRED_FIELDS_ERROR_MESSAGE, key="active_title"
            )

        # All validations passed
        self.logger.info("Validation successful")
        return self.data

    def create(self):
        """
        Persist user column preferences into DB.

        - Uses the validated data from `validate`.
        - Calls `create_or_update_table_column_fields` to insert/update preferences.
        - Logs the update for auditing.

        Returns:
            dict: Final data payload (including active/inactive titles and pagination).
        """
        self.logger.debug("Starting create operation")

        # Fetch feature and user
        feature_instance: CoreUtilsFeaturesModel = self.feature_queryset.get(
            title=self.data["feature"]
        )
        user_instance: UserModel = self.context["request"].user
        self.logger.debug(
            f"User: {user_instance.username}, Feature: {feature_instance.title}"
        )

        # Log current state
        try:
            table_order_instance: UserConfigTableOrderModel = (
                UserConfigTableOrderModel.objects.get(
                    user=user_instance, feature=feature_instance
                )
            )
            before_state: UserConfigTableFieldsModel = (
                UserConfigTableFieldsModel.objects.filter(
                    table=table_order_instance
                ).values("title", "is_active", "order")
            )
            self.logger.debug(f"Before state: {list(before_state)}")
        except UserConfigTableOrderModel.DoesNotExist:
            self.logger.debug("No existing table order instance found")

        # Save/update preferences in DB
        try:
            table_order_instance: UserConfigTableOrderModel = (
                create_or_update_table_column_fields(
                    feature_instance=feature_instance,
                    user_instance=user_instance,
                    active_title=self.active_title,
                    in_active_title=self.in_active_title,
                    pagination_count=self.data["pagination_count"],
                )
            )
        except Exception as e:
            self.logger.error(f"Failed to update preferences: {str(e)}")
            raise

        # Log final state
        after_state: List[str] = UserConfigTableFieldsModel.objects.filter(
            table=table_order_instance
        ).values("title", "is_active", "order")
        self.logger.debug(f"After state: {list(after_state)}")

        # Log success
        self.logger.info(
            f"UserConfig columns updated for user: {user_instance.username}, feature: {feature_instance.title}"
        )

        return self.data
