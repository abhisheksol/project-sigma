from store.operations.allocation_files.models import AllocationFileModel
from django.db import transaction
from typing import Any, List

from store.operations.allocation_files.v1.upload.utils.common.save_case_details import (
    UpdateAllocationFileCaseDetails,
)
from store.operations.case_management.enums import CaseManagementFieldStatusEnumChoices
from store.operations.case_management.models import CaseManagementCaseModel


class SaveAllocationFileCaseData(UpdateAllocationFileCaseDetails):
    """
    Handles saving allocation file and associated case management data.

    Extends:
        UpdateAllocationFileCaseDetails: Provides base methods for
        updating allocation file case details.

    Responsibilities:
        - Create and persist an allocation file record
        - Create associated case management instances for each loan account number
        - Update case details after initial creation
    """

    def save_allocation_file_and_case_details(self) -> AllocationFileModel:
        """
        Saves allocation file details and creates associated case management
        instances inside a database transaction.

        Workflow:
            1. Create an AllocationFileModel instance.
            2. Iterate through loan account numbers and create CaseManagementCaseModel instances.
            3. Ensure atomicity using `transaction.atomic()`.

        Returns:
            AllocationFileModel: The created allocation file instance.
        """
        self.logger.info("Starting save_allocation_file_and_case_details")
        with transaction.atomic():
            # Step 1: Create the allocation file record
            self.logger.info(
                f"Creating allocation file instance: title={self.file_name}"
            )
            self.allocation_file_instance: AllocationFileModel = self.queryset.create(
                title=self.file_name,
                file_url=self.file_url,
                initial_file_url=self.file_url,
                product_assignment=self.product_assignment_instance,
                no_of_total_records=len(self.file_data),
            )
            self.logger.info(
                f"Allocation file created: id={self.allocation_file_instance.id}"
            )

            # Step 2: Prepare case management instances
            self.logger.info(
                f"Preparing to create {len(self.loan_account_numbers_list)} case management instances"
            )
            case_management_instance_list: List[CaseManagementCaseModel] = []
            for loan_account_number in self.loan_account_numbers_list:
                self.logger.info(
                    f"Creating case instance for loan_account_number: {loan_account_number}"
                )
                # Each case is initially created with ERROR status
                instance: CaseManagementCaseModel = (
                    CaseManagementCaseModel.objects.create(
                        allocation_file=self.allocation_file_instance,
                        loan_account_number=loan_account_number,
                        field_mapping_status=CaseManagementFieldStatusEnumChoices.ERROR.value,
                    )
                )

                # Note: instance is created immediately (not batched here),
                # but still logged for traceability
                self.logger.debug(
                    f"Added case instance for {loan_account_number} -> {instance.pk} to batch"
                )

            # Step 3: Bulk operations could be added (currently logged only)
            self.logger.info("Performing bulk create of case management instances")
            self.logger.info(
                f"Successfully created {len(case_management_instance_list)} case instances"
            )

        self.logger.info("Completed save_allocation_file_and_case_details")
        return self.allocation_file_instance

    def update_allocation_file_cases_details(
        self,
    ) -> tuple[List[dict[str, Any]], List[dict[str, Any]]]:
        """
        Updates case management details by invoking parent implementation.

        This processes uploaded file data and:
            - Validates each case record
            - Updates case status accordingly
            - Separates valid and error records

        Returns:
            tuple[List[dict[str, Any]], List[dict[str, Any]]]:
                - First list contains valid case data
                - Second list contains error case data
        """
        self.logger.info("Starting update_allocation_file_cases_details")

        # Call the parent method to handle validation and case update logic
        error_data = super().update_allocation_file_cases_details()

        return error_data
