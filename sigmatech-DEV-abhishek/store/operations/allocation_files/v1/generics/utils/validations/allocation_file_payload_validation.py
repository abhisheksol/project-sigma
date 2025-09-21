from core_utils.utils.format_validator import is_format_validator_url
from core_utils.utils.global_variables import STATUS_ACTIVATED_GLOBAL_FILTERSET
from store.configurations.loan_config.template_config.enums import (
    CustomAllocatinFileTemplateStatusEnum,
)
from store.configurations.loan_config.template_config.models import (
    ProcessTemplatePreferenceModel,
)
from store.operations.allocation_files.v1.generics.utils.constants import (
    ALLOCATION_FILE_IS_REQUIRED_FIELD_ERROR_MESSAGE,
    ALLOCATION_FILE_MONTHLY_CYCLE_INCORRECT_ERROR_MESSAGE,
    ALLOCATION_FILE_NAME_EXISTS_ERROR_MESSAGE,
    ALLOCATION_FILE_NAME_IS_REQUIRED_FIELD_ERROR_MESSAGE,
    ALLOCATION_FILE_PROCESS_ID_INCORRECT_ERROR_MESSAGE,
    ALLOCATION_FILE_PRODUCT_ASSIGNMENT_INCORRECT_ERROR_MESSAGE,
    ALLOCATION_FILE_PRODUCT_ID_INCORRECT_ERROR_MESSAGE,
    INCORRECT_ALLOCATION_FILE_URL_FORMAT_ERROR_MESSAGE,
    INCORRECT_TEMPLATE_INACTIVE_FOR_PROCESS_ASSIGNED_PRODUCT_ERROR_MESSAGE,
)
from store.configurations.loan_config.models import (
    LoanConfigurationsMonthlyCycleModel,
    LoanConfigurationsProcessModel,
    LoanConfigurationsProductAssignmentModel,
    LoanConfigurationsProductsModel,
)
from store.configurations.loan_config.api.v1.utils.constants import (
    MONTHLY_CYCLE_ID_REQUIRED_ERROR_MESSAGE,
    PRODUCT_ID_REQUIRED_ERROR_MESSAGE,
    PROCESS_ID_REQUIRED_ERROR_MESSAGE,
)
from typing import Dict, Callable, Optional


class UploadAllocationFilePayloadValidation:
    """
    Handles validation for allocation file upload payload.

    This validator checks:
      - Required fields are present
      - File URL is correctly formatted and unique
      - File name does not already exist
      - Loan configuration fields (process, product, cycle, product assignment) are valid
    """

    # Required field mapping: field name -> error message if missing
    required_fields: Dict[str, str] = {
        "file_url": ALLOCATION_FILE_IS_REQUIRED_FIELD_ERROR_MESSAGE,
        "file_name": ALLOCATION_FILE_NAME_IS_REQUIRED_FIELD_ERROR_MESSAGE,
        "cycle_id": MONTHLY_CYCLE_ID_REQUIRED_ERROR_MESSAGE,
        "product_id": PRODUCT_ID_REQUIRED_ERROR_MESSAGE,
        "process_id": PROCESS_ID_REQUIRED_ERROR_MESSAGE,
    }

    def file_validations(self) -> Optional[Dict[str, str]]:
        """
        Validate file-specific rules:
          - File URL format
          - File name uniqueness

        Returns:
            Optional[Dict[str, str]]: Error message with the invalid key if validation fails,
                                      None otherwise.
        """
        if not is_format_validator_url(self.data["file_url"]):
            return {
                "error_message": INCORRECT_ALLOCATION_FILE_URL_FORMAT_ERROR_MESSAGE,
                "key": "file_url",
            }
        if self.queryset.filter(title=self.data["file_name"]).exists():
            return {
                "error_message": ALLOCATION_FILE_NAME_EXISTS_ERROR_MESSAGE,
                "key": "file_name",
            }

    def loan_config_field_validations(self) -> Optional[Dict[str, str]]:
        """
        Validate loan configuration references:
          - Process exists and is active
          - Product exists and is active
          - Monthly cycle exists and is active
          - Process and product assignment exists and is active

        Returns:
            Optional[Dict[str, str]]: Error message with the invalid key if validation fails,
                                      None otherwise.
        """
        if not LoanConfigurationsProcessModel.objects.filter(
            pk=self.data["process_id"],
            **STATUS_ACTIVATED_GLOBAL_FILTERSET,
        ).exists():
            return {
                "error_message": ALLOCATION_FILE_PROCESS_ID_INCORRECT_ERROR_MESSAGE,
                "key": "process_id",
            }

        if not LoanConfigurationsProductsModel.objects.filter(
            pk=self.data["product_id"],
            **STATUS_ACTIVATED_GLOBAL_FILTERSET,
        ).exists():
            return {
                "error_message": ALLOCATION_FILE_PRODUCT_ID_INCORRECT_ERROR_MESSAGE,
                "key": "product_id",
            }

        try:
            self.cycle_instance: LoanConfigurationsMonthlyCycleModel = (
                LoanConfigurationsMonthlyCycleModel.objects.get(
                    pk=self.data["cycle_id"],
                    **STATUS_ACTIVATED_GLOBAL_FILTERSET,
                )
            )
        except LoanConfigurationsMonthlyCycleModel.DoesNotExist:
            return {
                "error_message": ALLOCATION_FILE_MONTHLY_CYCLE_INCORRECT_ERROR_MESSAGE,
                "key": "cycle_id",
            }

        try:
            self.product_assignment_instance: (
                LoanConfigurationsProductAssignmentModel
            ) = LoanConfigurationsProductAssignmentModel.objects.get(
                process__pk=self.data["process_id"],
                product__pk=self.data["product_id"],
                **STATUS_ACTIVATED_GLOBAL_FILTERSET,
            )
        except LoanConfigurationsProductAssignmentModel.DoesNotExist:
            return {
                "error_message": ALLOCATION_FILE_PRODUCT_ASSIGNMENT_INCORRECT_ERROR_MESSAGE,
                "key": "product_id",
            }

        try:
            self.template_instance: ProcessTemplatePreferenceModel = (
                ProcessTemplatePreferenceModel.objects.get(
                    product_assignment=self.product_assignment_instance,
                    is_default=True,
                    status=CustomAllocatinFileTemplateStatusEnum.SUBMITTED.value,
                )
            )
        except ProcessTemplatePreferenceModel.DoesNotExist:
            return {
                "error_message": INCORRECT_TEMPLATE_INACTIVE_FOR_PROCESS_ASSIGNED_PRODUCT_ERROR_MESSAGE,
                "key": "process_id",
            }

    def validation_methods(self) -> Dict[Callable, Dict]:
        """
        Collect all validation methods to be executed.

        Reusable Method:
            Designed for extensibility.
            Subclasses can override this to add/remove validation methods
            without modifying the `is_valid` loop.

        Returns:
            Dict[Callable, Dict]: Dictionary of validation methods with arguments.
        """
        return {
            self.required_field_validation: {},
            self.file_validations: {},
            self.loan_config_field_validations: {},
        }
