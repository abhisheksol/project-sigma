from typing import Any, Callable, Dict, List, Optional
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

from store.operations.allocation_files.v1.upload.utils.common.excel_utils import (
    AllocationFileExcelUtils,
)
from store.operations.allocation_files.v1.upload.utils.save.update_allocation_file import (
    SaveReUploadAllocationFileCaseData,
)
from store.operations.allocation_files.v1.upload.utils.validations.reupload.payload import (
    ReUploadAllocationFilePayloadValidator,
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


class ReUploadAllocationFileHandler(
    ReUploadAllocationFilePayloadValidator,
    AllocationFileHeaderValidator,
    SaveReUploadAllocationFileCaseData,
    CoreGenericBaseHandler,
    AllocationFileExcelUtils,
):
    """
    Handler class for re-uploading Allocation Files.

    Responsibilities:
    - Extract and validate data from uploaded Excel allocation files.
    - Perform payload, header, and template-level validations.
    - Save validated case records into case management tables.
    - Track and update allocation file metadata (valid/error record counts, status).
    - Generate error files for invalid records.

    Inherits multiple mixins for validations, Excel utilities, and saving logic.
    """

    # Attribute annotations for clarity
    template_header_data: List[str]
    file_url: str
    allocation_file_id: str
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
    validated_data: List[Dict[str, str]] = []  # Stores successfully validated rows
    error_data: List[Dict[str, Any]] = []  # Stores rows with validation errors
    loan_account_numbers_list: List[Dict[str, Any]] = []  # Stores loan account numbers
    template_instance: ProcessTemplatePreferenceModel

    # QuerySets for related models
    case_management_queryset: QuerySet[CaseManagementCaseModel] = (
        CaseManagementCaseModel.objects.all()
    )
    address_type_queryset: QuerySet[AddressTypeModel] = AddressTypeModel.objects.all()
    pincode_queryset: QuerySet[RegionConfigurationPincodeModel] = (
        RegionConfigurationPincodeModel.objects.all()
    )
    case_management_address_queryset: QuerySet[CaseManagementCaseAddressModel] = (
        CaseManagementCaseAddressModel.objects.all()
    )

    # Default reserved headers from enum
    default_headers: List[str] = core_utils_list_enum_keys(
        enum_cls=CustomAllocationFileTemplateReservedFieldsEnum
    )

    # Activity monitoring metadata
    _activity_type: str = "UPLOAD_ALLOCATION_FILE_ACTVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.UPDATE.value

    def set_init_values(self):
        """
        Initialize key values from `self.data`.
        Expected fields: file_url, allocation_file_id.
        """
        print("self.data", self.data)
        self.file_url = self.data.get("file_url")
        self.allocation_file_id = self.data.get("allocation_file_id")
        # Example value: 'AXIS_CREDIT_CARD_19_09_2025'

    def validate(self):
        """
        Run validations in sequential order:
        1. Extract Excel data
        2. File-level validations
        3. Loan config field validations
        4. Header validation
        5. Template header validation
        6. Loan account number validations

        Returns:
            Error message dict if validation fails,
            otherwise None.
        """
        print(1)
        self.set_init_values()
        print(2)

        # List of validation methods executed sequentially
        validation_methods: List[Callable] = [
            self.extract_data_from_excel,
            self.file_validations,
            self.loan_config_field_validations,
            self.validate_header,
            self.template_excel_headers,
            self.upload_allocation_loan_acc_no_validation,
        ]

        print(3)
        # Run validations and capture error message if any
        error_message: Optional[Dict[str, str]] = (
            self.is_validation_list_of_methods_valid(
                validation_methods=validation_methods
            )
        )
        print("error_message", error_message)

        if error_message:
            # Return formatted error response
            return self.set_error_message(**error_message)

    def create(self):
        """
        Create or update allocation file records after successful validation:
        - Save allocation cases and return error data.
        - Generate error Excel file and update allocation file instance.
        - Update record counts (valid, error, total).
        - Update allocation status if all records are valid.
        - Persist changes to the database.
        """
        # Save allocation file cases and get error/valid data
        error_data: tuple[List[dict[str, Any]], List[dict[str, Any]]] = (
            self.update_allocation_file_cases_details()
        )
        print("update_allocation_file_cases_details")

        # Generate error Excel file and update allocation file instance
        excel_url: str = self.get_data_to_excel_url(error_data=error_data)
        print("a")
        self.allocation_file_instance.latest_error_file_url = excel_url

        # Count valid records
        self.allocation_file_instance.no_of_valid_records = (
            self.case_management_queryset.filter(
                allocation_file=self.allocation_file_instance,
                field_mapping_status=CaseManagementFieldStatusEnumChoices.SAVED.value,
            ).count()
        )
        print("b")

        # Count error records
        self.allocation_file_instance.no_of_error_records = (
            self.case_management_queryset.filter(
                allocation_file=self.allocation_file_instance,
                field_mapping_status=CaseManagementFieldStatusEnumChoices.ERROR.value,
            ).count()
        )
        print("c")

        # Update allocation status if all records are valid
        if (
            self.allocation_file_instance.no_of_total_records
            == self.allocation_file_instance.no_of_valid_records
        ):
            self.allocation_file_instance.allocation_status = (
                AllocationStatusEnum.INPROCESS.value
            )
        print("d")

        # Save allocation file instance with updated metadata

        # Update error file URL in response data
        self.data["error_file_url"] = (
            self.allocation_file_instance.latest_error_file_url
        )
        self.data["allocation_file_id"] = str(self.allocation_file_instance.pk)

        # Update created_by field for audit logging
        self.update_core_generic_updated_by(instance=self.allocation_file_instance)
        self.allocation_file_instance.save()
