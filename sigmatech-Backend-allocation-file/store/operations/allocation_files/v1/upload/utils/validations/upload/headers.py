from typing import Dict

from store.configurations.loan_config.template_config.enums import (
    CustomAllocationFileTemplateReservedFieldsEnum,
)
from store.operations.allocation_files.v1.upload.utils.common.constants import (
    LOAN_ACCOUNT_NUMBER_DUPLICATE_ERROR_MESSAGE,
    MISSING_REQUIRED_HEADERS_ERROR_MESSAGE,
)
from store.operations.allocation_files.v1.upload.utils.common.excel_utils import (
    AllocationFileExcelUtils,
)
from store.operations.case_management.enums import (
    CaseLifecycleStageEnum,
)


class AllocationFileHeaderValidator(AllocationFileExcelUtils):
    """
    Provides validations for allocation file headers and loan account numbers.
    Extends:
        AllocationFileExcelUtils: Utility class for working with Excel data.
    """

    def template_excel_headers(self):
        """
        Validate whether all required template headers are present in the uploaded file.

        Returns:
            dict: Error message if required headers are missing, otherwise empty dict.
        """
        # If any required header is missing in the file's header data, return an error
        if not any(
            i not in self.header_data for i in self.template_required_header_data
        ):
            return {
                "error_message": MISSING_REQUIRED_HEADERS_ERROR_MESSAGE,
                "key": "file_url",
            }
        # No issues with headers
        return {}

    def upload_allocation_loan_acc_no_validation(self):
        """
        Validate loan account numbers in the uploaded allocation file.

        Steps:
            1. Validate uniqueness of loan account numbers in the file itself.
            2. Check if any loan account number already exists in case management
               with a 'SAVED' status.

        Returns:
            dict: Error message if duplicates are found, otherwise empty dict.
        """
        # Step 1: Check for duplicates within the uploaded file
        error_message: Dict[str, str] = self.loan_account_number_validation()
        if error_message:
            return error_message

        # Step 2: Check if loan account numbers already exist in saved cases
        if (
            self.case_management_queryset.filter(
                **{
                    f"{CustomAllocationFileTemplateReservedFieldsEnum.LOAN_ACCOUNT_NUMBER.value}__in": self.loan_account_numbers_list,
                }
            )
            .exclude(status__title=CaseLifecycleStageEnum.FLOW.value)
            .exists()
        ):
            return {
                "error_message": LOAN_ACCOUNT_NUMBER_DUPLICATE_ERROR_MESSAGE,
                "key": "file_url",
            }

        # No validation errors
        return {}
