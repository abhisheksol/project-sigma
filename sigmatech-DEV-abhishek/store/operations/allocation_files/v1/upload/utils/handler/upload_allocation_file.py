import time
from typing import Any, Callable, Dict, List, Optional, Tuple
from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.enums import core_utils_list_enum_keys
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from store.configurations.loan_config.models import (
    LoanConfigurationsProcessModel,
    LoanConfigurationsProductAssignmentModel,
    LoanConfigurationsProductsModel,
)
from store.configurations.loan_config.template_config.enums import (
    CustomAllocationFileTemplateReservedFieldsEnum,
)
from store.configurations.loan_config.template_config.models import (
    ProcessTemplatePreferenceModel,
)
from store.configurations.region_config.models import RegionConfigurationPincodeModel
from store.operations.allocation_files.models import AllocationFileModel
from store.operations.allocation_files.v1.upload.utils.validations.upload.payload import (
    UploadAllocationFilePayloadValidator,
)

from store.operations.allocation_files.v1.upload.utils.common.excel_utils import (
    AllocationFileExcelUtils,
)
from store.operations.allocation_files.v1.upload.utils.save.save_allocation_file import (
    SaveAllocationFileCaseData,
)
from store.operations.allocation_files.v1.upload.utils.validations.upload.headers import (
    AllocationFileHeaderValidator,
)
from store.operations.allocation_files.v1.utils.enums import AllocationStatusEnum
from store.operations.case_management.enums import CaseManagementFieldStatusEnumChoices
from store.operations.case_management.models import (
    AddressTypeModel,
    CaseManagementCaseAddressModel,
    CaseManagementCaseModel,
)
from django.db.models.query import QuerySet


class UploadAllocationFileHandler(
    AllocationFileHeaderValidator,
    UploadAllocationFilePayloadValidator,
    SaveAllocationFileCaseData,
    CoreGenericBaseHandler,
    AllocationFileExcelUtils,
):
    """
    Handles the workflow for validating and creating Allocation File uploads.

    Inherits functionality from multiple mixins:
        - AllocationFileHeaderValidator: Validates file headers.
        - UploadAllocationFilePayloadValidator: Validates request payload.
        - SaveAllocationFileCaseData: Saves allocation file and related cases.
        - CoreGenericBaseHandler: Provides generic create/update handlers.
        - AllocationFileExcelUtils: Excel/CSV parsing utilities.

    Responsibilities:
        - Extract data from uploaded Excel/CSV file.
        - Validate headers, payloads, and loan configurations.
        - Save allocation file and related case details.
        - Track error/valid records and generate error files.

    Attributes:
        file_url (str): Uploaded file URL.
        file_name (str): Name of the uploaded file.
        product_title (str): Title of product linked to the file.
        process_title (str): Title of process linked to the file.
        headers (List[str]): Extracted header fields.
        file_data (List[Dict[str, str]]): Raw file data.
        validated_data (List[Dict[str, str]]): Validated data after processing.
        error_data (List[Dict[str, Any]]): Records containing errors.
        loan_account_numbers_list (List[Dict[str, Any]]): List of loan account numbers extracted from file.
        template_instance (ProcessTemplatePreferenceModel): Related template preference instance.
        allocation_file_instance (AllocationFileModel): Allocation file DB record.
        Various queryset attributes provide DB access to related models.
    """

    template_header_data: List[str]
    file_url: str
    file_name: str
    product_title: str
    process_title: str
    headers: List[str]
    process_instance: LoanConfigurationsProcessModel
    product_instance: LoanConfigurationsProductsModel
    allocation_file_instance: AllocationFileModel
    product_assignment_instance: LoanConfigurationsProductAssignmentModel
    file_data: List[Dict[str, str]]
    header_data: List[Dict[str, str]]
    template_header_data: List[Dict[str, str]]
    template_required_header_data: List[Dict[str, str]]
    validated_data: List[Dict[str, str]] = []
    error_data: List[Dict[str, Any]] = []
    loan_account_numbers_list: List[Dict[str, Any]] = []
    template_instance: ProcessTemplatePreferenceModel

    # Querysets for related models
    case_management_queryset: QuerySet[CaseManagementCaseModel] = (
        CaseManagementCaseModel.objects.select_related("allocation_file").all()
    )
    address_type_queryset: QuerySet[AddressTypeModel] = AddressTypeModel.objects.all()
    pincode_queryset: QuerySet[RegionConfigurationPincodeModel] = (
        RegionConfigurationPincodeModel.objects.all()
    )
    case_management_address_queryset: QuerySet[CaseManagementCaseAddressModel] = (
        CaseManagementCaseAddressModel.objects.all()
    )

    # Default headers derived from enum of reserved fields
    default_headers: List[str] = core_utils_list_enum_keys(
        enum_cls=CustomAllocationFileTemplateReservedFieldsEnum
    )

    # Activity monitoring metadata
    _activity_type: str = "UPLOAD_ALLOCATION_FILE_ACTVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.CREATE.value

    def set_init_values(self):
        """
        Initializes basic values from incoming data payload.
        Extracts file_url and file_name from request data.
        """
        print("self.data", self.data)
        self.file_url = self.data.get("file_url")
        self.file_name = self.data.get("file_name")
        # Example: 'AXIS_CREDIT_CARD_19_09_2025'

    def validate(self):
        """
        Executes all validation steps required before creating allocation file.

        Steps:
            1. Extract Excel/CSV data.
            2. Perform file validations.
            3. Validate loan configuration fields.
            4. Validate headers.
            5. Match template headers.
            6. Validate loan account numbers.

        Returns:
            Optional[Dict[str, str]]: Error message dict if any validation fails,
                                      otherwise None.
        """
        print(1)
        self.set_init_values()
        print(2)

        # List of validation methods to execute in sequence
        validation_methods: List[Callable] = [
            self.extract_data_from_excel,
            self.file_validations,
            self.loan_config_field_validations,
            self.validate_header,
            self.template_excel_headers,
            self.upload_allocation_loan_acc_no_validation,
        ]
        print(3)

        # Execute validations and check for error
        error_message: Optional[Dict[str, str]] = (
            self.is_validation_list_of_methods_valid(
                validation_methods=validation_methods
            )
        )
        print("error_message", error_message)

        # If any validation failed, return formatted error response
        if error_message:
            return self.set_error_message(**error_message)

    def create(self):
        """
        Persists allocation file and related case data.

        Workflow:
            1. Save allocation file and case details.
            2. Update case details linked to allocation file.
            3. Generate error file for failed records.
            4. Update allocation file record with counts and statuses.
            5. Save final record and update creator info.
        """
        # Step 1: Save allocation file and related case details
        start_time: time.time = time.time()
        self.save_allocation_file_and_case_details()
        print(
            f"save_allocation_file_and_case_details execution time: {time.time() - start_time:.2f} seconds"
        )

        # Step 2: Update case details, returns (valid_data, error_data)
        start_time: time.time = time.time()
        error_data: Tuple[List[dict[str, Any]], List[dict[str, Any]]] = (
            self.update_allocation_file_cases_details()
        )
        print(
            f"update_allocation_file_cases_details execution time: {time.time() - start_time:.2f} seconds"
        )

        # Step 3: Generate error Excel and update file URL
        start_time: time.time = time.time()
        excel_url: str = self.get_data_to_excel_url(error_data=error_data)
        print(
            f"get_data_to_excel_url execution time: {time.time() - start_time:.2f} seconds"
        )
        self.allocation_file_instance.latest_error_file_url = excel_url

        # Step 4: Count valid records
        start_time: time.time = time.time()
        self.allocation_file_instance.no_of_valid_records = (
            self.case_management_queryset.filter(
                allocation_file=self.allocation_file_instance,
                field_mapping_status=CaseManagementFieldStatusEnumChoices.SAVED.value,
            ).count()
        )
        print(
            f"Count valid records execution time: {time.time() - start_time:.2f} seconds"
        )

        # Step 5: Count error records
        start_time: time.time = time.time()
        self.allocation_file_instance.no_of_error_records = (
            self.case_management_queryset.filter(
                allocation_file=self.allocation_file_instance,
                field_mapping_status=CaseManagementFieldStatusEnumChoices.ERROR.value,
            ).count()
        )
        print(
            f"Count error records execution time: {time.time() - start_time:.2f} seconds"
        )

        # Step 6: Check if all records are valid and update status
        start_time: time.time = time.time()
        if (
            self.allocation_file_instance.no_of_total_records
            == self.allocation_file_instance.no_of_valid_records
        ):
            self.allocation_file_instance.allocation_status = (
                AllocationStatusEnum.INPROCESS.value
            )
        print(
            f"Check and update allocation status execution time: {time.time() - start_time:.2f} seconds"
        )

        # Step 7: Save allocation file record
        start_time: time.time = time.time()
        self.allocation_file_instance.save()
        self.data["allocation_file_id"] = str(self.allocation_file_instance.pk)
        print(
            f"Save allocation file record execution time: {time.time() - start_time:.2f} seconds"
        )

        # Step 8: Store error file URL in response data
        start_time: time.time = time.time()
        self.data["error_file_url"] = (
            self.allocation_file_instance.latest_error_file_url
        )
        print(
            f"Store error file URL execution time: {time.time() - start_time:.2f} seconds"
        )

        # Step 9: Update created_by field for audit trail
        start_time: time.time = time.time()
        self.update_core_generic_created_by(instance=self.allocation_file_instance)
        print(
            f"update_core_generic_created_by execution time: {time.time() - start_time:.2f} seconds"
        )

    # def create(self):
    #     """
    #     Persists allocation file and related case data.

    #     Workflow:
    #         1. Save allocation file and case details.
    #         2. Update case details linked to allocation file.
    #         3. Generate error file for failed records.
    #         4. Update allocation file record with counts and statuses.
    #         5. Save final record and update creator info.
    #     """
    #     # Save allocation file and related case details
    #     self.save_allocation_file_and_case_details()

    #     # Update case details, returns (valid_data, error_data)
    #     error_data: Tuple[List[dict[str, Any]], List[dict[str, Any]]] = (
    #         self.update_allocation_file_cases_details()
    #     )
    #     print("update_allocation_file_cases_details time calculation ")

    #     # Generate error Excel and update file URL
    #     excel_url: str = self.get_data_to_excel_url(error_data=error_data)
    #     print("a")
    #     self.allocation_file_instance.latest_error_file_url = excel_url

    #     # Count valid records
    #     self.allocation_file_instance.no_of_valid_records = (
    #         self.case_management_queryset.filter(
    #             allocation_file=self.allocation_file_instance,
    #             field_mapping_status=CaseManagementFieldStatusEnumChoices.SAVED.value,
    #         ).count()
    #     )
    #     print("b")

    #     # Count error records
    #     self.allocation_file_instance.no_of_error_records = (
    #         self.case_management_queryset.filter(
    #             allocation_file=self.allocation_file_instance,
    #             field_mapping_status=CaseManagementFieldStatusEnumChoices.ERROR.value,
    #         ).count()
    #     )
    #     print("c")

    #     # If all records are valid → mark as PROCESSED
    #     if (
    #         self.allocation_file_instance.no_of_total_records
    #         == self.allocation_file_instance.no_of_valid_records
    #     ):
    #         self.allocation_file_instance.allocation_status = (
    #             AllocationStatusEnum.PROCESSED.value
    #         )
    #     print("d")

    #     # Save allocation file record
    #     self.allocation_file_instance.save()
    #     self.data["allocation_file_id"] = str(self.allocation_file_instance.pk)

    #     # Store error file URL in response data
    #     self.data["error_file_url"] = (
    #         self.allocation_file_instance.latest_error_file_url
    #     )

    #     # Update created_by field for audit trail
    #     self.update_core_generic_created_by(instance=self.allocation_file_instance)
