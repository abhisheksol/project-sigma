from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.enums import CoreUtilsStatusEnum, list_enum_values
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler

from store.configurations.loan_config.api.v1.utils.constants import (
    PROCESS_ID_REQUIRED_ERROR_MESSAGE,
    PROCESS_NOT_FOUND_ERROR_MESSAGE,
    PROCESS_STATUS_INVALID_ERROR_MESSAGE,
    PROCESS_TITLE_ALREADY_EXISTS_ERROR_MESSAGE,
)
from django.db import transaction
from store.configurations.loan_config.models import LoanConfigurationsProcessModel
from typing import Union


class ProcessUpdateHandler(CoreGenericBaseHandler):
    """
    Handler for updating an existing LoanConfigurationsProcessModel instance.

    Inherits from:
        CoreGenericBaseHandler – Provides base error handling and common response utilities.

    Responsibilities:
        - Validates input data before update.
        - Ensures the given ID exists in the database.
        - Ensures status value (if provided) is valid.
        - Updates the model instance inside an atomic transaction.
    """

    _activity_type: str = "CONFIGURATION_PROCESS_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.UPDATE.value

    def validate(self):
        """
        Validates the incoming data for updating a LoanConfigurationsProcessModel.

        Checks:
            - 'id' is provided.
            - The instance with given 'id' exists in the queryset.
            - 'status' (if present) is either 'ACTIVATED' or 'DEACTIVATED'.

        Returns:
            Sets error messages using `set_error_message` if validation fails.
        """
        # Ensure the 'id' is provided in the payload
        if not self.data.get("id"):
            return self.set_error_message(PROCESS_ID_REQUIRED_ERROR_MESSAGE, key="id")

        # Check whether the process with the given 'id' exists
        if not self.queryset.filter(id=self.data["id"]).exists():
            return self.set_error_message(PROCESS_NOT_FOUND_ERROR_MESSAGE, key="id")

        title: Union[str, None] = self.data.get("title")
        if (
            title
            and self.queryset.filter(title__iexact=title)
            .exclude(id=self.data["id"])
            .exists()
        ):
            return self.set_error_message(
                PROCESS_TITLE_ALREADY_EXISTS_ERROR_MESSAGE, key="title"
            )

        # Optional: Validate status if provided
        if self.data.get("status") and self.data.get("status") not in list_enum_values(
            enum_cls=CoreUtilsStatusEnum
        ):
            return self.set_error_message(
                PROCESS_STATUS_INVALID_ERROR_MESSAGE, key="status"
            )

        self.context["logger"].info("Validating Process Update Handler")

    def create(self):
        """
        Updates an existing LoanConfigurationsProcessModel instance.

        Uses:
            `self.update_model_instance()` utility for performing field-level updates.

        Executes inside a Django atomic transaction block to maintain data integrity.
        """
        with transaction.atomic():
            # Fetch the instance using the given ID
            instance: LoanConfigurationsProcessModel = self.queryset.get(
                id=self.data["id"]
            )

            # Update instance fields using reusable utility
            self.update_model_instance(instance=instance, data=self.data)

            self.context["logger"].info(
                f"Process updated successfully. Process ID : {instance.pk}"
            )
