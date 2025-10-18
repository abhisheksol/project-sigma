from store.configurations.loan_config.models import (
    LoanConfigurationsProductAssignmentModel,
)
from typing import Dict, Optional, List
from core_utils.utils.format_validator import is_format_validator_url
from core_utils.utils.global_variables import STATUS_ACTIVATED_GLOBAL_FILTERSET
from store.configurations.loan_config.template_config.enums import (
    CustomAllocationFileTemplateReservedFieldsEnum,
)
from store.configurations.loan_config.template_config.models import (
    ProcessTemplatePreferenceModel,
)
from store.operations.allocation_files.v1.upload.utils.common.constants import (
    ALLOCATION_FILE_IS_REQUIRED_FIELD_ERROR_MESSAGE,
    ALLOCATION_FILE_PRODUCT_ASSIGNMENT_INCORRECT_ERROR_MESSAGE,
    EMPTY_ALLOCATION_FILE_ERROR_MESSAGE,
    INCORRECT_ALLOCATION_FILE_URL_FORMAT_ERROR_MESSAGE,
    INCORRECT_TEMPLATE_INACTIVE_FOR_PROCESS_ASSIGNED_PRODUCT_ERROR_MESSAGE,
    MULTIPLE_PROCESS_NAME_EXCEL_ERROR_MESSAGE,
    MULTIPLE_PRODUCT_TYPE_EXCEL_ERROR_MESSAGE,
    PROCESS_NAME_IS_MISSING_IN_EXCEL_ERROR_MESSAGE,
    PRODUCT_TYPE_IS_MISSING_IN_EXCEL_ERROR_MESSAGE,
)
from store.operations.allocation_files.v1.upload.utils.template_utils import (
    get_default_process_product_assigned_template_instance,
)


class AllocationFilePayloadValidator:
    """
    Handles validation for allocation file upload payload.

    This validator checks:
      - Required fields are present
      - File URL is correctly formatted
      - Product assignment and loan configuration fields are valid
      - Template associated with the process/product is active
      - Single unique process and product exist in the uploaded Excel/CSV file
    """

    # Required field mapping: field name -> error message if missing
    required_fields: Dict[str, str] = {
        "file_url": ALLOCATION_FILE_IS_REQUIRED_FIELD_ERROR_MESSAGE,
    }

    def file_validations(self) -> Optional[Dict[str, str]]:
        """
        Validate file-specific rules:
          - File URL format is correct

        Returns:
            Optional[Dict[str, str]]: Error message with the invalid key if validation fails,
                                      None otherwise.
        """
        if not is_format_validator_url(self.data["file_url"]):
            error: Dict[str, str] = {
                "error_message": INCORRECT_ALLOCATION_FILE_URL_FORMAT_ERROR_MESSAGE,
                "key": "file_url",
            }
            self.logger.debug(f"File validation result: {error}")
            return error

        self.logger.debug("File validation passed")
        return None

    def loan_config_field_validations(self) -> Optional[Dict[str, str]]:
        """
        Validate loan configuration references:
          - Process exists and is active
          - Product exists and is active
          - Product assignment exists and is active
          - Associated template for the assignment is active

        Returns:
            Optional[Dict[str, str]]: Error message with the invalid key if validation fails,
                                      None otherwise.
        """
        # Validate required fields first
        error_message: Dict[str, str] = self.required_field_validation(
            required_fields=self.required_fields
        )
        if error_message:
            return error_message

        try:
            # Check product assignment validity
            product_assignment_values_error: str = self.is_product_assignment_valid()
            if product_assignment_values_error:
                error: Dict[str, str] = {
                    "error_message": product_assignment_values_error,
                    "key": "file_url",
                }
                self.logger.debug(f"Loan config validation result: {error}")
                return error

            # Fetch the active product assignment instance
            self.product_assignment_instance: (
                LoanConfigurationsProductAssignmentModel
            ) = LoanConfigurationsProductAssignmentModel.objects.get(
                process__title=self.process_title,
                product__title=self.product_title,
                **STATUS_ACTIVATED_GLOBAL_FILTERSET,
            )

        except LoanConfigurationsProductAssignmentModel.DoesNotExist:
            # Product assignment does not exist or is inactive
            error: Dict[str, str] = {
                "error_message": ALLOCATION_FILE_PRODUCT_ASSIGNMENT_INCORRECT_ERROR_MESSAGE,
                "key": "file_url",
            }
            self.logger.debug(f"Loan config validation result: {error}")
            return error

        try:
            # Fetch the default active template associated with the process/product
            self.template_instance: ProcessTemplatePreferenceModel = (
                get_default_process_product_assigned_template_instance(
                    product_assignment_instance=self.product_assignment_instance
                )
            )

        except ProcessTemplatePreferenceModel.DoesNotExist:
            # Template does not exist or is inactive
            error: Dict[str, str] = {
                "error_message": INCORRECT_TEMPLATE_INACTIVE_FOR_PROCESS_ASSIGNED_PRODUCT_ERROR_MESSAGE,
                "key": "file_url",
            }
            self.logger.debug(f"Loan config validation result: {error}")
            return error

        self.logger.debug("Loan config validation passed")
        return None

    def _get_set_of_values(self, field_name: str) -> List:
        """
        Helper method to get the unique set of values for a given field
        from the file data.

        Args:
            field_name (str): Column name in the file.

        Returns:
            List: Unique values present in the column.
        """
        return list(set([i[field_name] for i in self.file_data]))

    def is_product_assignment_valid(self) -> Optional[str]:
        """
        Validate that uploaded file contains a single process and product type,
        and that the required columns are present.

        Checks:
          - File is not empty
          - Process name and product type columns exist
          - Only one unique process name exists
          - Only one unique product type exists

        Returns:
            Optional[str]: Error message string if validation fails, None otherwise.
        """
        print("is_product_assignment_valid")

        # Check if file has any rows
        if len(self.file_data) < 1:
            return EMPTY_ALLOCATION_FILE_ERROR_MESSAGE

        # Validate required headers
        if (
            CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.name
            not in self.header_data
        ):
            return PROCESS_NAME_IS_MISSING_IN_EXCEL_ERROR_MESSAGE

        if (
            CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.name
            not in self.header_data
        ):
            return PRODUCT_TYPE_IS_MISSING_IN_EXCEL_ERROR_MESSAGE

        # Validate single unique process
        if (
            len(
                self._get_set_of_values(
                    field_name=CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.name
                )
            )
            != 1
        ):
            return MULTIPLE_PROCESS_NAME_EXCEL_ERROR_MESSAGE

        # Validate single unique product type
        if (
            len(
                self._get_set_of_values(
                    field_name=CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.name
                )
            )
            != 1
        ):
            return MULTIPLE_PRODUCT_TYPE_EXCEL_ERROR_MESSAGE

        # Set process and product titles from the first row
        self.product_title = self.file_data[0][
            CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.name
        ]
        self.process_title = self.file_data[0][
            CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.name
        ]
