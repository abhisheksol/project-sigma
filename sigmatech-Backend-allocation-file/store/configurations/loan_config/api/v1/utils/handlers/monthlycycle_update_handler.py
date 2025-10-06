from django.db import transaction

from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.enums import CoreUtilsStatusEnum, list_enum_values
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler

from store.configurations.loan_config.api.v1.utils.constants import (
    MONTHLY_CYCLE_ID_REQUIRED_ERROR_MESSAGE,
    MONTHLY_CYCLE_NOT_FOUND_ERROR_MESSAGE,
    MONTHLY_CYCLE_STATUS_INVALID_ERROR_MESSAGE,
    MONTHLY_CYCLE_TITLE_ALREADY_EXISTS_ERROR_MESSAGE,
)
from store.configurations.loan_config.models import LoanConfigurationsMonthlyCycleModel
from typing import Union


class MonthlyCycleUpdateHandler(CoreGenericBaseHandler):
    """
    Handler to update an existing Monthly Cycle configuration.

    Responsibilities:
        - Validates existence and correctness of the provided data.
        - Updates the record using a utility function inside a transaction block.
    """

    _activity_type: str = "CONFIGURATION_MONTHLY_CYCLE_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.UPDATE.value

    def validate(self):
        """
        Validates incoming update data before applying changes.

        Checks:
            - 'id' must be present in the request.
            - A Monthly Cycle must exist with the given 'id'.
            - 'status' (if provided) must be either 'ACTIVATED' or 'DEACTIVATED'.

        Returns:
            Sets an error message via `self.set_error_message()` if validation fails.
        """

        # Check if 'id' is provided
        if not self.data.get("id"):
            return self.set_error_message(
                MONTHLY_CYCLE_ID_REQUIRED_ERROR_MESSAGE, key="id"
            )

        # Check if Monthly Cycle with given 'id' exists
        if not self.queryset.filter(id=self.data["id"]).exists():
            return self.set_error_message(
                MONTHLY_CYCLE_NOT_FOUND_ERROR_MESSAGE, key="id"
            )

        title: Union[int, None] = self.data.get("title")
        print(1)
        if (
            title is not None
            and self.queryset.filter(title=title).exclude(id=self.data["id"]).exists()
        ):
            return self.set_error_message(
                MONTHLY_CYCLE_TITLE_ALREADY_EXISTS_ERROR_MESSAGE, key="title"
            )

        # Validate status (if provided)
        if self.data.get("status") and self.data.get("status") not in list_enum_values(
            enum_cls=CoreUtilsStatusEnum
        ):
            return self.set_error_message(
                MONTHLY_CYCLE_STATUS_INVALID_ERROR_MESSAGE, key="status"
            )

        self.context["logger"].info("Validating Monthly Cycle Update Handler")

    def create(self):
        """
        Updates the Monthly Cycle instance with new values.

        Performs the update inside a Django atomic transaction block to ensure consistency.

        Uses:
            - `self.update_model_instance()` to apply partial updates to the model.
        """
        with transaction.atomic():

            # Fetch the existing instance by ID
            instance: LoanConfigurationsMonthlyCycleModel = self.queryset.get(
                id=self.data["id"]
            )

            # Update fields using shared utility
            self.update_model_instance(instance=instance, data=self.data)

            self.context["logger"].info(
                f"Monthly Cycle updated successfully. Monthly Cycle ID : {instance.pk}"
            )
