from typing import Any, List

from store.operations.allocation_files.v1.upload.utils.common.save_case_details import (
    UpdateAllocationFileCaseDetails,
)


class SaveReUploadAllocationFileCaseData(UpdateAllocationFileCaseDetails):
    """
    Extends UpdateAllocationFileCaseDetails to handle saving and updating case details
    specifically for re-uploaded allocation files.

    This class provides functionality for reprocessing case management data
    when an allocation file is re-uploaded, leveraging the parent class logic
    while adding logging and potential hooks for additional handling.
    """

    def update_allocation_file_cases_details(
        self,
    ) -> tuple[List[dict[str, Any]], List[dict[str, Any]]]:
        """
        Updates case management details for a re-uploaded allocation file.

        This method:
          - Logs the update operation.
          - Delegates the main update logic to the parent class implementation.
          - Ensures validated data and error data are properly returned.

        Returns:
            tuple[List[dict[str, Any]], List[dict[str, Any]]]:
                A tuple containing:
                  - Validated data (records successfully updated).
                  - Error data (records with validation or mapping errors).
        """
        self.logger.info("Starting update_allocation_file_cases_details")

        # Call parent class's update method, which performs
        # validation and persistence of allocation file case data
        error_data = super().update_allocation_file_cases_details()

        # Return the result for further handling (e.g., error reporting, persistence)
        return error_data
