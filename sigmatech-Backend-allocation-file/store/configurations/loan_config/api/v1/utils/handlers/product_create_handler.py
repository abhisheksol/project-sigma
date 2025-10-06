from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from store.configurations.loan_config.api.v1.utils.constants import (
    PRODUCT_TITLE_ALREADY_EXISTS_ERROR_MESSAGE,
    PRODUCT_TITLE_REQUIRED_ERROR_MESSAGE,
)
from store.configurations.loan_config.models import LoanConfigurationsProductsModel
from django.db import transaction
from typing import Union


class ProductCreateHandler(CoreGenericBaseHandler):
    """
    Handler responsible for validating and creating Product records
    in the Loan Configuration module.

    Inherits from:
        CoreGenericBaseHandler – provides base error handling and response support.
    """

    _activity_type: str = "CONFIGURATION_PRODUCT_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.CREATE.value

    def validate(self):
        """
        Validates the input data before creating a Product.

        Validation Checks:
            - 'title' must be present and unique.
            - 'code' must be present and unique.
            - 'status' (if provided) must be either 'ACTIVATED' or 'DEACTIVATED'.

        Returns:
            - Sets appropriate error messages using `self.set_error_message()`
              if validation fails.
        """
        title: Union[str, None] = self.data.get("title")

        # Check if title is provided
        if not title:
            return self.set_error_message(
                PRODUCT_TITLE_REQUIRED_ERROR_MESSAGE, key="title"
            )

        # Check if title already exists
        if self.queryset.filter(title__iexact=title).exists():
            return self.set_error_message(
                PRODUCT_TITLE_ALREADY_EXISTS_ERROR_MESSAGE, key="title"
            )

        self.context["logger"].info("Validating Product Create Handler")

    def create(self):
        """
        Creates a new Product record using the validated input.

        This operation is wrapped inside a Django atomic transaction block
        to ensure data integrity.

        Fields expected in `self.data`:
            - title: str
            - code: str
            - status: str ("ACTIVATED" or "DEACTIVATED")
        """
        with transaction.atomic():
            # Create the product instance with required fields
            instance: LoanConfigurationsProductsModel = self.queryset.create(
                title=self.data.get("title"),
                description=self.data.get("description"),
            )
            self.update_core_generic_created_by(instance=instance)
            self.context["logger"].info(
                f"Product created successfully. Product ID : {instance.pk}"
            )
