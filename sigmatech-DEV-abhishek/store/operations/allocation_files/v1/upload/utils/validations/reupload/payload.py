from typing import Dict, Optional
from core_utils.utils.format_validator import is_format_validator_url

from store.operations.allocation_files.models import AllocationFileModel
from store.operations.allocation_files.v1.upload.utils.common.constants import (
    ALLOCATION_FILE_HAS_NO_ERROR_RECORDS_ERROR_MESSAGE,
    ALLOCATION_FILE_IS_REQUIRED_FIELD_ERROR_MESSAGE,
    ALLOCATION_ID_IS_REQUIRED_FIELD_ERROR_MESSAGE,
    INCORRECT_ALLOCATION_FILE_ID_ERROR_MESSAGE,
    INCORRECT_ALLOCATION_FILE_URL_FORMAT_ERROR_MESSAGE,
)
from store.operations.allocation_files.v1.upload.utils.common.payload_validator import (
    AllocationFilePayloadValidator,
)
from store.operations.case_management.enums import CaseManagementFieldStatusEnumChoices


class ReUploadAllocationFilePayloadValidator(AllocationFilePayloadValidator):
    """
    Validator for re-uploading allocation file payloads.

    Responsibilities:
    - Ensure required fields (file URL, allocation file ID) are provided.
    - Validate the format of the file URL.
    - Ensure allocation file ID exists in the database.
    - Ensure the allocation file has error records to allow re-upload.
    """

    # Mapping of required payload fields to their corresponding error messages
    required_fields: Dict[str, str] = {
        "allocation_file_id": ALLOCATION_ID_IS_REQUIRED_FIELD_ERROR_MESSAGE,
        "file_url": ALLOCATION_FILE_IS_REQUIRED_FIELD_ERROR_MESSAGE,
    }

    def file_validations(self) -> Optional[Dict[str, str]]:
        """
        Perform file-level validations for re-uploading an allocation file.

        Validation checks:
            1. File URL format is valid.
            2. Allocation file ID exists in the database.
            3. Allocation file has error records (since only error records can be corrected and re-uploaded).

        Returns:
            Optional[Dict[str, str]]:
                - Returns an error dictionary with "error_message" and "key" if validation fails.
                - Returns None if all validations pass.
        """
        self.logger.info("file_validations")

        # 1. Validate file URL format
        if not is_format_validator_url(self.data["file_url"]):
            error: Dict[str, str] = {
                "error_message": INCORRECT_ALLOCATION_FILE_URL_FORMAT_ERROR_MESSAGE,
                "key": "file_url",
            }
            self.logger.debug(f"File validation result: {error}")
            return error

        # 2. Validate allocation file ID existence
        try:
            self.allocation_file_instance: AllocationFileModel = self.queryset.get(
                pk=self.data["allocation_file_id"]
            )
        except AllocationFileModel.DoesNotExist:
            error: Dict[str, str] = {
                "error_message": INCORRECT_ALLOCATION_FILE_ID_ERROR_MESSAGE,
                "key": "allocation_file_id",
            }
            self.logger.debug(f"File validation result: {error}")
            return error

        # 3. Validate that the allocation file has error records
        if not self.case_management_queryset.filter(
            allocation_file=self.allocation_file_instance,
            field_mapping_status=CaseManagementFieldStatusEnumChoices.ERROR.value,
        ).exists():
            error: Dict[str, str] = {
                "error_message": ALLOCATION_FILE_HAS_NO_ERROR_RECORDS_ERROR_MESSAGE,
                "key": "allocation_file_id",
            }
            self.logger.debug(f"File validation result: {error}")
            return error

        # All validations passed
        self.logger.debug("File validation passed")
        return None
