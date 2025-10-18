from typing import Any, Dict, List, Optional
import requests
from requests.models import Response

import pandas as pd
from pandas.core.frame import DataFrame
from core_utils.utils.enums import get_enum_value_with_key
from core_utils.utils.excel_utils import dataframe_to_records_json
from store.configurations.loan_config.template_config.enums import (
    CustomAllocationFileTemplateReservedFieldsEnum,
)
from store.operations.allocation_files.v1.upload.utils.common.constants import (
    FILE_EMPTY_ERROR_MESSAGE,
    FILE_READ_ERROR_MESSAGE,
    LOAN_ACCOUNT_DUPLICATE_NUMBER_ERROR_MESSAGE,
    LOAN_ACCOUNT_NUMBER_MISSING_ERROR_MESSAGE,
    LOAN_ACCOUNT_NUMBER_REQUIRED_ERROR_MESSAGE,
    UNEXPECTED_HEADERS_ERROR_MESSAGE,
    UNSUPPORTED_FILE_FORMAT_ERROR_MESSAGE,
    EXTRA_HEADERS_RECEIVED_ERROR_MESSAGE,
)
from store.operations.allocation_files.v1.upload.utils.template_utils import (
    get_template_fields_list,
    get_template_required_fields_list,
)

from core_utils.utils.file_utils.extract import (
    fetch_dataframe_from_url,
    fetch_field_exclude_nan_values_from_url,
)


class AllocationFileExcelUtils:
    """
    Utility class for handling Excel/CSV file extraction, header validation,
    and loan account number validation for allocation files.

    Provides helper methods to:
      - Fetch and parse file data from a URL into DataFrame.
      - Validate file format, headers, and required fields.
      - Validate loan account numbers (existence, uniqueness, no missing values).
    """

    def extract_data_from_excel(self) -> Optional[Dict[str, str]]:
        """
        Extracts headers and data from an Excel/CSV file and validates file format.

        Process:
          - Checks if file extension is supported (.xlsx, .xls, .csv).
          - Fetches file content from URL.
          - Reads file into a DataFrame and extracts headers and data.
          - Returns error if file is empty or unreadable.

        Returns:
            Optional[Dict[str, str]]: Error message with invalid key if validation fails,
                                      None otherwise.
        """
        try:
            # Detect file type from extension
            file_extension: str = self.file_url.lower().split(".")[-1]
            self.logger.debug(f"Detected file extension: {file_extension}")

            # Validate allowed file extensions
            if file_extension not in ["xlsx", "xls", "csv"]:
                error: Dict[str, str] = {
                    "error_message": UNSUPPORTED_FILE_FORMAT_ERROR_MESSAGE,
                    "key": "file_url",
                }
                self.logger.debug(f"Header validation result: {error}")
                return error

            # Fetch file content from the provided URL
            response: Response = requests.get(self.file_url, stream=True)
            response.raise_for_status()
            self.logger.debug("Successfully fetched file content from URL.")

            # Convert file into pandas DataFrame
            df: DataFrame = fetch_dataframe_from_url(file_url=self.data["file_url"])
            print("df", df)

            # Extract headers and data
            self.header_data: List[str] = df.columns.tolist()
            print("self.headers", self.header_data)
            self.file_data: List[Dict[str, Any]] = dataframe_to_records_json(df=df)

            self.logger.debug(f"Extracted headers: {self.header_data}")

            # Validate if headers are present
            if not self.header_data:
                error: Dict[str, str] = {
                    "error_message": FILE_EMPTY_ERROR_MESSAGE,
                    "key": "file_url",
                }
                self.logger.debug(f"Header validation result: {error}")
                return error

            return None

        except pd.errors.EmptyDataError as e:
            # Handles case when file is empty
            error: Dict[str, str] = {
                "error_message": FILE_EMPTY_ERROR_MESSAGE,
                "key": "file_url",
            }
            self.logger.debug(f"Header validation result: {error}, {str(e)}")
            return error
        except Exception as e:
            # Generic error while reading file
            error: Dict[str, str] = {
                "error_message": FILE_READ_ERROR_MESSAGE,
                "key": "file_url",
            }
            self.logger.debug(f"Header validation result: {error}, {str(e)}")
            return error

    def validate_header(self) -> Dict[str, str]:
        """
        Validates headers in the uploaded file against expected/default headers.

        Process:
          - Ensures no extra headers beyond expected ones.
          - Ensures headers are valid and expected.
          - Loads template header data and required template headers for validation.

        Returns:
            Dict[str, str]: Error message if headers are invalid, empty dict otherwise.
        """

        # Check if file has more headers than expected
        if len(self.default_headers) < len(self.header_data):
            return {
                "error_message": EXTRA_HEADERS_RECEIVED_ERROR_MESSAGE,
                "key": "file_url",
            }

        # Fetch template-specific headers for the product assignment
        self.template_header_data: List[str] = get_template_fields_list(
            product_assignment_instance=self.product_assignment_instance
        )

        for i in self.header_data:
            if (
                get_enum_value_with_key(
                    enum_class=CustomAllocationFileTemplateReservedFieldsEnum, key=i
                )
                not in self.template_header_data
            ):
                return {
                    "error_message": f"{UNEXPECTED_HEADERS_ERROR_MESSAGE} {i}",
                    "key": "file_url",
                }
        if len(self.template_header_data) < len(self.header_data):
            return {
                "error_message": EXTRA_HEADERS_RECEIVED_ERROR_MESSAGE,
                "key": "file_url",
            }
        self.template_required_header_data: List[str] = (
            get_template_required_fields_list(
                product_assignment_instance=self.product_assignment_instance
            )
        )
        return {}

    def loan_account_number_validation(self) -> Dict[str, str]:
        """
        Validates loan account number column in the file.

        Process:
          - Ensures the loan account number column exists in headers.
          - Extracts loan account numbers from the file, excluding NaN values.
          - Validates no missing loan account numbers.
          - Validates loan account numbers are unique.

        Returns:
            Dict[str, str]: Error message if validation fails, empty dict otherwise.
        """
        loan_account_number_field_name: str = (
            CustomAllocationFileTemplateReservedFieldsEnum.LOAN_ACCOUNT_NUMBER.name
        )

        # Check if loan account number column is present
        if loan_account_number_field_name not in self.header_data:
            return {
                "error_message": LOAN_ACCOUNT_NUMBER_REQUIRED_ERROR_MESSAGE,
                "key": "file_url",
            }

        # Extract loan account numbers, excluding NaN
        self.loan_account_numbers_list: List[str] = (
            fetch_field_exclude_nan_values_from_url(
                file_url=self.file_url,
                field_name=CustomAllocationFileTemplateReservedFieldsEnum.LOAN_ACCOUNT_NUMBER.name,
            )
        )

        # Validate no missing loan account numbers
        if len(self.file_data) != len(self.loan_account_numbers_list):
            return {
                "error_message": LOAN_ACCOUNT_NUMBER_MISSING_ERROR_MESSAGE,
                "key": "file_url",
            }

        # Validate uniqueness of loan account numbers
        if len(self.file_data) != len(set(self.loan_account_numbers_list)):
            return {
                "error_message": LOAN_ACCOUNT_DUPLICATE_NUMBER_ERROR_MESSAGE,
                "key": "file_url",
            }

        return {}
