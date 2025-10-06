from django.db import transaction
from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.enums import CoreUtilsStatusEnum, list_enum_values
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from core_utils.utils.global_variables import STATUS_ACTIVATED_GLOBAL_FILTERSET

from store.configurations.loan_config.api.v1.utils.constants import (
    MIN_MAX_DUE_PERCENTAGE_ERROR_MESSAGE,
    PROCESS_ID_NOT_FOUND_ERROR_MESSAGE,
    PRODUCT_ASSIGNMENT_ALREADY_EXISTS_ERROR_MESSAGE,
    PRODUCT_ASSIGNMENT_NOT_FOUND_ERROR_MESSAGE,
    PRODUCT_ASSIGNMENT_STATUS_INVALID_ERROR_MESSAGE,
    PRODUCT_ID_NOT_FOUND_ERROR_MESSAGE,
)
from store.configurations.loan_config.models import (
    LoanConfigurationsProcessModel,
    LoanConfigurationsProductAssignmentModel,
    LoanConfigurationsProductsModel,
)
from typing import Union, Dict
from copy import deepcopy


class ProductAssignmentUpdateHandler(CoreGenericBaseHandler):
    """
    Handler to validate and update an existing ProductAssignment instance.
    This represents a link between a product and a process with associated attributes like min_due_percentage, status, etc.
    """

    # Cached model instances after validation for efficiency
    process_instance: Union[LoanConfigurationsProcessModel, None] = None
    product_instance: Union[LoanConfigurationsProductsModel, None] = None
    assignment_instance: Union[LoanConfigurationsProductAssignmentModel, None] = None

    # Activity log type and method for tracking the update action
    _activity_type: str = "CONFIGURATION_PRODUCT_ASSIGNMENT_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.UPDATE.value

    def validate(self):
        """
        Validates the incoming data for updating a ProductAssignment.
        - Ensures the assignment ID is provided and exists.
        - Ensures that the process and product IDs are valid if provided.
        - Checks that a product assignment record exists for the given process-product combination.
        """
        assignment_id: str = self.data.get("id")
        process_uuid: Union[str, None] = self.data.get("process")
        product_uuid: Union[str, None] = self.data.get("product")
        min_due_percentage: Union[float, None] = float(
            self.data.get("min_due_percentage", 0)
        )
        refer_back_percentage: Union[float, None] = float(
            self.data.get("refer_back_percentage", 0)
        )

        # Step 1: Ensure the assignment ID is provided
        if not assignment_id:
            return self.set_error_message(
                error_message=PRODUCT_ASSIGNMENT_NOT_FOUND_ERROR_MESSAGE
            )

        # Step 2: Validate the process if provided
        if process_uuid:
            try:
                # Fetch the LoanConfigurationsProcessModel instance based on UUID
                self.process_instance = LoanConfigurationsProcessModel.objects.get(
                    pk=process_uuid, **STATUS_ACTIVATED_GLOBAL_FILTERSET
                )
            except LoanConfigurationsProcessModel.DoesNotExist:
                return self.set_error_message(
                    PROCESS_ID_NOT_FOUND_ERROR_MESSAGE, key="process"
                )

        # Step 3: Validate the product if provided
        if product_uuid:
            try:
                # Fetch the LoanConfigurationsProductsModel instance based on UUID
                self.product_instance = LoanConfigurationsProductsModel.objects.get(
                    pk=product_uuid, **STATUS_ACTIVATED_GLOBAL_FILTERSET
                )
            except LoanConfigurationsProductsModel.DoesNotExist:
                return self.set_error_message(
                    PRODUCT_ID_NOT_FOUND_ERROR_MESSAGE, key="product"
                )

        # Step 4: Validate the status if provided
        if self.data.get("status") and self.data["status"] not in list_enum_values(
            enum_cls=CoreUtilsStatusEnum
        ):
            return self.set_error_message(
                PRODUCT_ASSIGNMENT_STATUS_INVALID_ERROR_MESSAGE, key="status"
            )
        if isinstance(min_due_percentage, float) and (
            min_due_percentage < 0 or min_due_percentage > 100
        ):
            return self.set_error_message(
                MIN_MAX_DUE_PERCENTAGE_ERROR_MESSAGE, key="min_due_percentage"
            )
        if isinstance(refer_back_percentage, float) and (
            refer_back_percentage < 0 or refer_back_percentage > 100
        ):
            return self.set_error_message(
                MIN_MAX_DUE_PERCENTAGE_ERROR_MESSAGE, key="refer_back_percentage"
            )

        # Step 5: Ensure the product assignment exists
        try:
            # Fetch the existing ProductAssignment instance using the assignment ID
            self.assignment_instance = (
                LoanConfigurationsProductAssignmentModel.objects.get(pk=assignment_id)
            )
            self.process_instance = (
                self.assignment_instance.process
            )  # Assign associated process instance

            # Check that the combination of process and product is unique
            if (
                product_uuid
                and LoanConfigurationsProductAssignmentModel.objects.exclude(
                    pk=assignment_id
                )
                .filter(process=self.process_instance, product=self.product_instance)
                .exists()
            ):
                return self.set_error_message(
                    PRODUCT_ASSIGNMENT_ALREADY_EXISTS_ERROR_MESSAGE, key="product"
                )

        except LoanConfigurationsProductAssignmentModel.DoesNotExist:
            return self.set_error_message(PRODUCT_ASSIGNMENT_NOT_FOUND_ERROR_MESSAGE)

    def create(self):
        """
        Updates the existing ProductAssignment instance using the validated incoming data.
        This function executes the update in a transactional context to ensure atomicity.
        """
        with transaction.atomic():
            # Step 1: Make a deep copy of the incoming data to avoid modifying the original data
            data: Dict = deepcopy(self.data)

            # Step 2: Replace UUIDs with model instances for related fields (process and product)
            if self.process_instance:
                data["process"] = self.process_instance
            if self.product_instance:
                data["product"] = self.product_instance

            # Step 3: Set a toast message value for UI feedback on the updated product
            self.set_toast_message_value(value=self.assignment_instance.product.title)

            # Step 4: Perform the actual update operation using the utility function
            self.update_model_instance(instance=self.assignment_instance, data=data)

            # Step 5: Log the successful update action for tracking
            self.context["logger"].info(
                f"Product Assignment updated successfully. ID: {self.assignment_instance.pk}"
            )
