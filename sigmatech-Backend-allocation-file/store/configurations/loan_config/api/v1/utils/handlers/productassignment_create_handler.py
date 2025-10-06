from typing import Union
from django.db import transaction
from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.enums import list_enum_values
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from core_utils.utils.global_variables import STATUS_ACTIVATED_GLOBAL_FILTERSET
from store.configurations.loan_config.api.v1.utils.constants import (
    MIN_MAX_DUE_PERCENTAGE_ERROR_MESSAGE,
    PROCESS_ID_NOT_FOUND_ERROR_MESSAGE,
    PROCESS_STATUS_INVALID_ERROR_MESSAGE,
    PRODUCT_ASSIGNMENT_ALREADY_EXISTS_ERROR_MESSAGE,
    PRODUCT_ID_NOT_FOUND_ERROR_MESSAGE,
)
from store.configurations.loan_config.models import (
    LoanConfigurationsProcessModel,
    LoanConfigurationsProductsModel,
    LoanConfigurationsProductAssignmentModel,
)


class ProductAssignmentCreateHandler(CoreGenericBaseHandler):
    """
    Handler to validate and create a ProductAssignment instance,
    which links a Product to a Process with defined business rules.
    """

    process_instance: LoanConfigurationsProcessModel
    product_instance: LoanConfigurationsProductsModel
    min_due_percentage: int
    refer_back_percentage: int

    _activity_type: str = "CONFIGURATION_PRODUCT_ASSIGNMENT_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.CREATE.value

    def validate(self):
        """
        Validates that:
        - The provided process ID exists.
        - The provided product ID exists.
        - The combination of process and product does not already exist.
        """
        self.logger.info("Validating Product Assignment Create Handler")
        self.min_due_percentage: float = float(self.data.get("min_due_percentage", 0))
        self.refer_back_percentage: float = float(
            self.data.get("refer_back_percentage", 0)
        )
        process_uuid: Union[str, None] = self.data.get("process")
        product_uuid: Union[str, None] = self.data.get("product")

        # Validate process instance existence
        try:
            self.process_instance: LoanConfigurationsProcessModel = (
                LoanConfigurationsProcessModel.objects.get(
                    pk=process_uuid, **STATUS_ACTIVATED_GLOBAL_FILTERSET
                )
            )

        except LoanConfigurationsProcessModel.DoesNotExist:
            return self.set_error_message(
                PROCESS_ID_NOT_FOUND_ERROR_MESSAGE, key="process"
            )

        # Validate product instance existence
        try:
            self.product_instance: LoanConfigurationsProductsModel = (
                LoanConfigurationsProductsModel.objects.get(
                    pk=product_uuid, **STATUS_ACTIVATED_GLOBAL_FILTERSET
                )
            )
        except LoanConfigurationsProductsModel.DoesNotExist:
            return self.set_error_message(
                PRODUCT_ID_NOT_FOUND_ERROR_MESSAGE, key="product"
            )

        # Check if the combination already exists
        if self.queryset.filter(
            process=self.process_instance, product=self.product_instance
        ).exists():
            return self.set_error_message(
                PRODUCT_ASSIGNMENT_ALREADY_EXISTS_ERROR_MESSAGE, key="product"
            )

        # Optional: Validate status if provided
        if self.data.get("status") and self.data.get("status") not in list_enum_values(
            enum_cls=LoanConfigurationsProductAssignmentModel
        ):
            return self.set_error_message(
                PROCESS_STATUS_INVALID_ERROR_MESSAGE, key="status"
            )

        # grater and less than 0
        if self.min_due_percentage <= 0 or self.min_due_percentage > 100:
            return self.set_error_message(
                MIN_MAX_DUE_PERCENTAGE_ERROR_MESSAGE, key="min_due_percentage"
            )

        if self.refer_back_percentage <= 0 or self.refer_back_percentage > 100:
            return self.set_error_message(
                MIN_MAX_DUE_PERCENTAGE_ERROR_MESSAGE, key="refer_back_percentage"
            )

    def create(self):
        """
        Creates the ProductAssignment instance after validation.
        Links the given product and process with `min_due_percentage` and `refer_back_percentage`.
        """
        self.logger.info("Creating Product Assignment")

        with transaction.atomic():
            instance: LoanConfigurationsProductAssignmentModel = self.queryset.create(
                process=self.process_instance,
                product=self.product_instance,
                min_due_percentage=self.min_due_percentage,
                refer_back_percentage=self.refer_back_percentage,
            )
            self.set_toast_message_value(value=instance.product.title)
            self.update_core_generic_created_by(instance=instance)

            self.logger.info(f"Product assignment created. ID: {instance.pk}")
            return instance
