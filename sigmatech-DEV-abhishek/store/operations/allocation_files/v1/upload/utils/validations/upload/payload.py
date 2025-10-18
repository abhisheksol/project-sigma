from typing import Dict, Optional
from core_utils.utils.format_validator import is_format_validator_url
from store.operations.allocation_files.v1.upload.utils.common.constants import (
    ALLOCATION_FILE_IS_REQUIRED_FIELD_ERROR_MESSAGE,
    ALLOCATION_FILE_NAME_EXISTS_ERROR_MESSAGE,
    ALLOCATION_FILE_NAME_IS_REQUIRED_FIELD_ERROR_MESSAGE,
    INCORRECT_ALLOCATION_FILE_URL_FORMAT_ERROR_MESSAGE,
)
from store.operations.allocation_files.v1.upload.utils.common.payload_validator import (
    AllocationFilePayloadValidator,
)


class UploadAllocationFilePayloadValidator(AllocationFilePayloadValidator):
    """
    Validator for allocation file upload payload.

    Responsibilities:
        - Ensure required fields (`file_url`, `file_name`) are present
        - Validate `file_url` format
        - Ensure `file_name` is unique (not already used)
        - Validate loan configuration fields
          (delegated to base class `AllocationFilePayloadValidator`)

    Attributes:
        required_fields (Dict[str, str]): Maps required field names to error messages
                                          when they are missing.
    """

    # Mapping of required fields with their corresponding error messages
    required_fields: Dict[str, str] = {
        "file_url": ALLOCATION_FILE_IS_REQUIRED_FIELD_ERROR_MESSAGE,
        "file_name": ALLOCATION_FILE_NAME_IS_REQUIRED_FIELD_ERROR_MESSAGE,
    }

    def file_validations(self) -> Optional[Dict[str, str]]:
        """
        Perform validation checks specific to the uploaded file.

        Steps:
            1. Validate that the file URL has the correct format.
            2. Validate that the file name is unique in the database.

        Returns:
            Optional[Dict[str, str]]:
                - A dictionary with `error_message` and `key` if validation fails.
                - None if all validations pass.
        """
        # Step 1: Validate file URL format
        if not is_format_validator_url(self.data["file_url"]):
            error: Dict[str, str] = {
                "error_message": INCORRECT_ALLOCATION_FILE_URL_FORMAT_ERROR_MESSAGE,
                "key": "file_url",
            }
            # Log validation failure for debugging
            self.logger.debug(f"File validation result: {error}")
            return error

        # Step 2: Ensure file name is unique
        if self.queryset.filter(title=self.data["file_name"]).exists():
            error: Dict[str, str] = {
                "error_message": ALLOCATION_FILE_NAME_EXISTS_ERROR_MESSAGE,
                "key": "file_name",
            }
            # Log validation failure for debugging
            self.logger.debug(f"File validation result: {error}")
            return error

        # If all validations pass, log success
        self.logger.debug("File validation passed")
        return None
