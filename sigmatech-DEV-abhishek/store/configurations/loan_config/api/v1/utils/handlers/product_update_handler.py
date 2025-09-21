from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from django.db import transaction


from store.configurations.loan_config.api.v1.utils.constants import (
    PRODUCT_ID_REQUIRED_ERROR_MESSAGE,
    PRODUCT_NOT_FOUND_ERROR_MESSAGE,
    PRODUCT_STATUS_INVALID_ERROR_MESSAGE,
    PRODUCT_TITLE_ALREADY_EXISTS_ERROR_MESSAGE,
)
from store.configurations.loan_config.models import LoanConfigurationsProductsModel
from typing import Union
from core_utils.utils.enums import CoreUtilsStatusEnum, list_enum_values


class ProductUpdateHandler(CoreGenericBaseHandler):
    """
    Handler for updating an existing LoanConfigurationsProductsModel instance.

    Responsibilities:
        - Validate the provided input data for update.
        - Ensure the product ID exists.
        - Perform the update transaction safely.
    """

    _activity_type: str = "CONFIGURATION_PRODUCT_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.UPDATE.value

    def validate(self):
        """
        Validates incoming data before updating the Product instance.

        Checks:
            - 'id' must be provided.
            - A product with the given 'id' must exist.
            - 'status' (if provided) must be either 'ACTIVATED' or 'DEACTIVATED'.

        Returns:
            - Sets appropriate error messages via `self.set_error_message()` if validation fails.
        """
        # Check if 'id' is provided
        if not self.data.get("id"):
            return self.set_error_message(PRODUCT_ID_REQUIRED_ERROR_MESSAGE, key="id")

        # Check if product with given 'id' exists
        if not self.queryset.filter(id=self.data["id"]).exists():
            return self.set_error_message(PRODUCT_NOT_FOUND_ERROR_MESSAGE, key="id")

        # Validate 'status' field if present
        if self.data.get("status") and self.data.get("status") not in list_enum_values(
            enum_cls=CoreUtilsStatusEnum
        ):
            return self.set_error_message(
                PRODUCT_STATUS_INVALID_ERROR_MESSAGE, key="status"
            )

        title: Union[str, None] = self.data.get("title")
        if (
            title
            and self.queryset.filter(title__iexact=title)
            .exclude(id=self.data["id"])
            .exists()
        ):
            return self.set_error_message(
                PRODUCT_TITLE_ALREADY_EXISTS_ERROR_MESSAGE, key="title"
            )

        self.context["logger"].info("Validating Product Update Handler")

    def create(self):
        """
        Updates the Product record in the database.

        Executes inside a Django atomic transaction to ensure database integrity.

        Uses:
            - `self.update_model_instance()` to update fields dynamically from the provided data.

        Expected fields in `self.data`:
            - id (required)
            - Any other fields to be updated (e.g., title, code, status)
        """
        with transaction.atomic():
            # Retrieve the existing product instance using the provided ID
            instance: LoanConfigurationsProductsModel = self.queryset.get(
                id=self.data["id"]
            )

            # Apply updates using the shared utility function
            self.update_model_instance(instance=instance, data=self.data)

            self.context["logger"].info(
                f"Product updated successfully. Product ID : {instance.pk}"
            )
