from copy import deepcopy
from typing import Dict, Union
from django.db import transaction

from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.enums import CoreUtilsStatusEnum, list_enum_values
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler

from store.configurations.loan_config.api.v1.utils.constants import (
    BUCKET_CYCLE_ID_REQUIRED_ERROR_MESSAGE,
    BUCKET_CYCLE_NOT_FOUND_ERROR_MESSAGE,
    BUCKET_RANGE_NOT_FOUND_ERROR_MESSAGE,
    BUCKET_STATUS_INVALID_ERROR_MESSAGE,
    BUCKET_TITLE_ALREADY_EXISTS_ERROR_MESSAGE,
)
from store.configurations.loan_config.models import (
    BucketRangeModel,
    LoanConfigurationsBucketModel,
)


class BucketUpdateHandler(CoreGenericBaseHandler):
    """
    Handler class responsible for validating and updating a Bucket Cycle
    in the Loan Configuration module.
    """

    _activity_type: str = "CONFIGURATION_BUCKET_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.UPDATE.value
    range_instance: BucketRangeModel = None

    def validate(self):
        """
        Validates the data required for updating a Bucket Cycle.

        Checks:
        - The `id` field must be present.
        - A Bucket Cycle with the given `id` must exist.
        - If `title` is being updated, it must remain unique.
        """
        range_id: Union[str] = self.data.get("range")
        if range_id:
            try:
                self.range_instance = BucketRangeModel.objects.get(id=range_id)
            except BucketRangeModel.DoesNotExist:
                return self.set_error_message(
                    BUCKET_RANGE_NOT_FOUND_ERROR_MESSAGE, key="range"
                )

        if not self.data.get("id"):
            return self.set_error_message(
                BUCKET_CYCLE_ID_REQUIRED_ERROR_MESSAGE, key="id"
            )

        # Ensure the bucket with the given ID exists
        if not self.queryset.filter(id=self.data["id"]).exists():
            return self.set_error_message(
                BUCKET_CYCLE_NOT_FOUND_ERROR_MESSAGE, key="id"
            )

        # Check for unique title if it's being updated
        title = self.data.get("title")
        if (
            title
            and self.queryset.filter(title__iexact=title)
            .exclude(id=self.data["id"])
            .exists()
        ):
            return self.set_error_message(
                BUCKET_TITLE_ALREADY_EXISTS_ERROR_MESSAGE, key="title"
            )

        # Optional: Validate status if provided
        if self.data.get("status") and self.data.get("status") not in list_enum_values(
            enum_cls=CoreUtilsStatusEnum
        ):
            return self.set_error_message(
                BUCKET_STATUS_INVALID_ERROR_MESSAGE, key="status"
            )

        self.context["logger"].info("Validating Bucket Cycle Update Handler")

    def create(self):
        """
        Updates the Bucket Cycle instance with the validated data.

        - Retrieves the instance by ID.
        - Applies updates using `self.update_model_instance`.
        - Saves the changes within an atomic transaction.
        """
        with transaction.atomic():
            # Fetch the current bucket instance
            instance: LoanConfigurationsBucketModel = self.queryset.get(
                id=self.data["id"]
            )

            data: Dict = deepcopy(self.data)

            # Replace UUIDs with model instances for related fields
            # if self.range_instance:
            #     data["range"] = self.range_instance

            # Perform the update with validated data
            self.update_model_instance(instance=instance, data=data)
            self.context["logger"].info(
                f"Bucket Cycle updated successfully. Bucket Cycle ID : {instance.pk}"
            )
