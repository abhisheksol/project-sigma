from copy import deepcopy
from typing import Dict, Union
from django.db import transaction

from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from store.configurations.loan_config.api.v1.utils.constants import (
    BUCKET_RANGE_NOT_FOUND_ERROR_MESSAGE,
    BUCKET_RANGE_REQUIRED_ERROR_MESSAGE,
    BUCKET_TITLE_ALREADY_EXISTS_ERROR_MESSAGE,
    BUCKET_TITLE_REQUIRED_ERROR_MESSAGE,
)
from store.configurations.loan_config.models import (
    BucketRangeModel,
    LoanConfigurationsBucketModel,
)


class BucketCreateHandler(CoreGenericBaseHandler):
    """
    Handler class for creating a new Bucket in the Loan Configuration module.

    Responsibilities:
    - Validate input data.
    - Ensure title is unique.
    - Save new bucket instance into the database.
    """

    _activity_type: str = "CONFIGURATION_BUCKET_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.CREATE.value

    range_instance: Union[BucketRangeModel, None] = [None]

    def validate(self):
        """
        Validates the input data required to create a Bucket.

        Checks:
        - `title` must be provided and unique.
        - `description` must be provided.
        """

        range_uuid: Union[str, None] = self.data.get("range")
        title: Union[str, None] = self.data.get("title")

        if range_uuid:
            try:
                self.range_instance = BucketRangeModel.objects.get(id=range_uuid)
            except BucketRangeModel.DoesNotExist:
                return self.set_error_message(
                    BUCKET_RANGE_NOT_FOUND_ERROR_MESSAGE, key="range"
                )
        else:
            return self.set_error_message(
                BUCKET_RANGE_REQUIRED_ERROR_MESSAGE, key="range"
            )

        # Validate presence of title
        if not title:
            return self.set_error_message(
                BUCKET_TITLE_REQUIRED_ERROR_MESSAGE, key="title"
            )

        # Validate title uniqueness
        if self.queryset.filter(title__iexact=title).exists():
            return self.set_error_message(
                BUCKET_TITLE_ALREADY_EXISTS_ERROR_MESSAGE, key="title"
            )

        self.context["logger"].info("Validating Bucket Create Handler")

    def create(self):
        """
        Creates and saves a new Bucket instance within a transaction.

        Fields:
        - title
        - description
        """
        with transaction.atomic():
            data: Dict = deepcopy(self.data)

            # Replace UUIDs with model instances for related fields
            if self.range_instance:
                data["range"] = self.range_instance

            # Perform create using shared utility
            instance: LoanConfigurationsBucketModel = self.queryset.create(**data)
            self.update_core_generic_created_by(instance=instance)

            self.context["logger"].info(
                f"Bucket created successfully. Bucket ID : {instance.pk}"
            )
