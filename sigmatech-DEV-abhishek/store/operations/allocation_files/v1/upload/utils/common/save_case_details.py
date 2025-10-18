from decimal import Decimal, DecimalException
from core_utils.media_storage.api.v1.utils.data_convertors import (
    convert_data_to_excel_file,
    upload_file_object_and_get_url,
)
from core_utils.utils.enums import get_enum_key_with_value, get_enum_value_with_key
from store.configurations.loan_config.models import (
    LoanConfigurationsBucketModel,
    LoanConfigurationsMonthlyCycleModel,
    LoanConfigurationsProcessModel,
    LoanConfigurationsProductAssignmentModel,
    LoanConfigurationsProductsModel,
)
from store.configurations.loan_config.template_config.enums import (
    CustomAllocationFileTemplateReservedFieldsEnum,
)
from store.configurations.region_config.models import RegionConfigurationPincodeModel
from store.operations.case_management.models import (
    CaseManagementCaseModel,
)
from store.operations.allocation_files.v1.upload.utils.risk_cal_utils import (
    calculate_risk_enum_for_case_instance,
)
from store.operations.case_management.enums import CaseManagementFieldStatusEnumChoices
from django.core.exceptions import ObjectDoesNotExist
from core_utils.utils.format_validator import (
    is_format_validator_email,
    is_format_validator_phone,
)
import datetime
from typing import List, Dict, Any, Optional, Tuple, Type


class Utils:
    """
    Utility methods for data validation, address handling, and error management.

    Provides helper methods for validating field types, converting data, generating error files,
    and retrieving related model instances. Used by classes handling allocation file uploads.

    Attributes:
        field_type_mapping (Dict[str, Tuple[Type, Optional[Dict[str, Any]]]]): Mapping of field names
            to their expected types and constraints (e.g., max_length, validation_method).
    """

    # Mapping of field names to their expected types and validation constraints
    field_type_mapping: Dict[str, Tuple[Type, Optional[Dict[str, Any]]]] = {
        "customer_name": (str, {"max_length": 255}),
        "father_name": (str, {"max_length": 255}),
        "customer_dob": (datetime.date, {}),
        "customer_personal_email_id": (
            str,
            {
                "max_length": 255,
                "is_email": True,
                "validation_method": is_format_validator_email,
            },
        ),
        "customer_pan_number": (str, {"max_length": 20}),
        "primary_number": (
            str,
            {
                "max_length": 20,
                "validation_method": is_format_validator_phone,
                "is_phone_number": True,
            },
        ),
        "alternate_number_1": (
            str,
            {
                "max_length": 20,
                "validation_method": is_format_validator_phone,
                "is_phone_number": True,
            },
        ),
        "alternate_number_2": (
            str,
            {
                "max_length": 20,
                "validation_method": is_format_validator_phone,
                "is_phone_number": True,
            },
        ),
        "alternate_number_3": (
            str,
            {
                "max_length": 20,
                "validation_method": is_format_validator_phone,
                "is_phone_number": True,
            },
        ),
        "alternate_number_4": (
            str,
            {
                "max_length": 20,
                "validation_method": is_format_validator_phone,
                "is_phone_number": True,
            },
        ),
        "customer_employer_office_name": (str, {"max_length": 255}),
        "customers_office_email_id": (
            str,
            {
                "max_length": 255,
                "is_email": True,
                "validation_method": is_format_validator_email,
            },
        ),
        "occupation_type": (str, {"max_length": 50}),
        "customer_bank": (str, {"max_length": 100}),
        "loan_account_number": (str, {"max_length": 50}),
        "card_number": (str, {"max_length": 50}),
        "crn_number": (str, {"max_length": 50}),
        "pool_type": (str, {"max_length": 50}),
        "vehicle_number": (str, {"max_length": 50}),
        "asset_make": (str, {"max_length": 100}),
        "tenure": (int, {}),
        "engineno": (str, {"max_length": 50}),
        "chassisno": (str, {"max_length": 50}),
        "credit_limit": (Decimal, {"max_digits": 15, "decimal_places": 2}),
        "cash_limit": (Decimal, {"max_digits": 15, "decimal_places": 2}),
        "total_loan_amount": (Decimal, {"max_digits": 15, "decimal_places": 2}),
        "pos_value": (Decimal, {"max_digits": 15, "decimal_places": 2}),
        "emi_amount": (Decimal, {"max_digits": 15, "decimal_places": 2}),
        "minimum_due_amount": (Decimal, {"max_digits": 15, "decimal_places": 2}),
        "collectable_amount": (Decimal, {"max_digits": 15, "decimal_places": 2}),
        "penalty_amount": (Decimal, {"max_digits": 15, "decimal_places": 2}),
        "late_payment_fee": (Decimal, {"max_digits": 15, "decimal_places": 2}),
        "late_payment_charges": (Decimal, {"max_digits": 15, "decimal_places": 2}),
        "number_of_emi_paid": (int, {}),
        "loan_disbursement_date": (datetime.date, {}),
        "maturity_date": (datetime.date, {}),
        "emi_start_date": (datetime.date, {}),
        "due_date": (datetime.date, {}),
        "last_payment_date": (datetime.date, {}),
        "last_purchase_date": (datetime.date, {}),
        "mob": (str, {"max_length": 100}),
        "reason_of_bounce_date": (datetime.date, {}),
        "last_payment_amount": (Decimal, {"max_digits": 15, "decimal_places": 2}),
        "last_purchase_amount": (Decimal, {"max_digits": 15, "decimal_places": 2}),
        "billing_cycle": (
            LoanConfigurationsMonthlyCycleModel,
            {
                "return_instance": lambda value, **kwargs: kwargs["model"].objects.get(
                    title=value
                ),
                "kwargs": {"model": LoanConfigurationsMonthlyCycleModel},
            },
        ),
        "risk_statement": (str, {}),
        "delinquency_string": (str, {"max_length": 255}),
        "current_dpd": (int, {}),
        "allocation_type": (str, {"max_length": 50}),
        "nach_status": (str, {"max_length": 50}),
        "reason_of_bounce": (str, {"max_length": 255}),
        "reference_name_1": (str, {"max_length": 255}),
        "reference_contact_number_1": (
            str,
            {"max_length": 20, "validation_method": is_format_validator_phone},
        ),
        "reference_name_2": (str, {"max_length": 255}),
        "reference_contact_number_2": (
            str,
            {"max_length": 20, "validation_method": is_format_validator_phone},
        ),
        "cycle": (
            LoanConfigurationsBucketModel,
            {
                "return_instance": lambda value, **kwargs: kwargs["model"].objects.get(
                    title=value
                ),
                "kwargs": {"model": LoanConfigurationsBucketModel},
            },
        ),
        "residential_address_1": (str, {"max_length": 255}),
        "residential_address_2": (str, {"max_length": 255}),
        "residential_address_3": (str, {"max_length": 255}),
        "residential_address_4": (str, {"max_length": 255}),
        "residential_customer_city": (str, {"max_length": 100}),
        "residential_customer_state": (str, {"max_length": 100}),
        "residential_pin_code": (
            RegionConfigurationPincodeModel,
            {
                "return_instance": lambda value, **kwargs: kwargs["model"].objects.get(
                    pincode__pincode=int(value)
                ),
                "kwargs": {"model": RegionConfigurationPincodeModel},
            },
        ),
        "residential_country": (str, {"max_length": 100}),
        "customer_employer_address_1": (str, {"max_length": 255}),
        "customer_employer_address_2": (str, {"max_length": 255}),
        "customer_employer_address_3": (str, {"max_length": 255}),
        "customer_employer_address_4": (str, {"max_length": 255}),
        "customer_office_city": (str, {"max_length": 100}),
        "customer_office_state": (str, {"max_length": 100}),
        "customer_office_pin_code": (
            RegionConfigurationPincodeModel,
            {
                "return_instance": lambda value, **kwargs: kwargs["model"].objects.get(
                    pincode__pincode=int(value)
                ),
                "kwargs": {"model": RegionConfigurationPincodeModel},
            },
        ),
        "customer_office_country": (str, {"max_length": 100}),
    }

    def _get_pincode_instance(
        self, pin_code: Optional[str]
    ) -> Optional[RegionConfigurationPincodeModel]:
        """
        Retrieves a pincode instance from the database based on the provided pincode value.

        Args:
            pin_code (Optional[str]): The pincode string to look up.

        Returns:
            Optional[RegionConfigurationPincodeModel]: The pincode model instance if found, None otherwise.

        Side Effects:
            - Logs debug messages indicating whether the pincode was found or not.
        """
        if not pin_code:
            self.logger.debug("No pincode provided, returning None")
            return None
        self.logger.debug(f"Fetching pincode: {pin_code}")
        # Query the pincode queryset for the given pincode
        instance: Optional[RegionConfigurationPincodeModel] = (
            self.pincode_queryset.filter(pincode=pin_code).first()
        )
        self.logger.debug(
            f"Pincode '{pin_code}': {'Found' if instance else 'Not found'}"
        )
        return instance

    def set_error(
        self, key: str, value: Any, error_fields: List[str], exception: str
    ) -> List[str]:
        """
        Logs an error for a field and appends it to the error_fields list.

        Args:
            key (str): The field name causing the error.
            value (Any): The invalid value for the field.
            error_fields (List[str]): List to append the error message to.
            exception (str): The error message or exception details.

        Returns:
            List[str]: The updated error_fields list with the new error appended.

        Side Effects:
            - Logs a warning with the error details.
            - Appends the error message to error_fields.
        """
        self.logger.warning(f"Error in field {key} with value {value}: {exception}")
        error_fields.append(key)
        return error_fields

    def _convert_value_for_field(
        self, field: str, value: Any, error_fields: List[str]
    ) -> Any:
        """
        Converts a value to the expected type for a given field, logging errors if conversion fails.

        Args:
            field (str): The name of the field to convert the value for.
            value (Any): The raw value to convert.
            error_fields (List[str]): List to append error messages if conversion fails.

        Returns:
            Any: The converted value if successful, None if conversion fails.

        Side Effects:
            - Logs debug messages for successful conversions.
            - Logs errors and appends to error_fields if conversion fails.
        """
        try:
            self.logger.info("_convert_value_for_field")
            # Get the expected type and constraints for the field
            expected_type, _ = self.field_type_mapping[field]
            if expected_type == datetime.date and isinstance(value, str):
                # Convert string to date using %Y-%m-%d format
                converted: datetime.date = datetime.datetime.strptime(
                    value, "%Y-%m-%d"
                ).date()
            elif expected_type == Decimal:
                # Convert value to Decimal
                converted: Decimal = Decimal(str(value))
            elif expected_type == int:
                # Convert value to integer
                converted: int = int(value)
            else:
                # Use the raw value for other types
                converted: Any = value
            self.logger.debug(
                f"Converted {field} from {type(value)} to {type(converted)}"
            )
            return converted
        except (ValueError, TypeError, DecimalException) as e:
            # Log and record conversion errors
            self.set_error(
                key=field,
                value=value,
                error_fields=error_fields,
                exception=f"Invalid {self.field_type_mapping[field][0].__name__} format: {str(e)}",
            )
            return None

    def get_data_to_excel_url(self, error_data: List[Dict[str, Any]]) -> str:
        """
        Converts error data into an Excel file and uploads it to storage, returning the URL.

        Args:
            error_data (List[Dict[str, Any]]): List of records with error messages.

        Returns:
            str: URL of the uploaded Excel file, or an empty string if no error data.

        Side Effects:
            - Creates an Excel file from error_data if present.
            - Uploads the file to storage and logs the resulting URL.
        """
        self.logger.info("Generating Excel file for error data")
        if not error_data:
            self.logger.info("No error data to convert, returning empty URL")
            return ""
        # Convert error data to an Excel file
        file_path: str = convert_data_to_excel_file(
            error_data, file_prefix="allocation_error"
        )
        self.logger.debug(f"Excel file created at path: {file_path}")
        # Upload the file and get the URL
        url: str = upload_file_object_and_get_url(self.request, file_path)
        self.logger.debug(f"Uploaded Excel file URL: {url}")
        return url


class UpdateAllocationFileCaseDetails(Utils):
    """
    Manages the validation and updating of case management details from uploaded allocation file data.

    This class processes records from `file_data`, validates field values against expected types and constraints,
    updates corresponding `CaseManagementCaseModel` instances, and tracks errors for generating error reports.
    It ensures consistency in product and process across all records and uses bulk database operations for efficiency.
    Risk-related fields (e.g., `risk`, `risk_points`) are included in updates to ensure they are saved correctly.
    The implementation avoids caching and constructor modifications, maintaining performance and compatibility.
    """

    def _get_product_assignment_instance(
        self, product: str, process: str
    ) -> Optional[LoanConfigurationsProductAssignmentModel]:
        """
        Retrieves a `LoanConfigurationsProductAssignmentModel` instance based on product and process titles.

        Queries the database for the specified product and process, then retrieves the associated product assignment.
        Sets instance attributes `product_instance` and `process_instance` if found.

        Args:
            product (str): The title of the product to query.
            process (str): The title of the process to query.

        Returns:
            Optional[LoanConfigurationsProductAssignmentModel]: The product assignment instance if found, else `None`.

        Side Effects:
            - Assigns `self.product_instance` and `self.process_instance` if the query is successful.
            - Logs an error if the product, process, or assignment is not found in the database.
        """
        try:
            self.product_instance: LoanConfigurationsProductsModel = (
                LoanConfigurationsProductsModel.objects.get(title=product)
            )
            self.process_instance: LoanConfigurationsProcessModel = (
                LoanConfigurationsProcessModel.objects.get(title=process)
            )
            return LoanConfigurationsProductAssignmentModel.objects.get(
                product=self.product_instance, process=self.process_instance
            )
        except ObjectDoesNotExist:
            self.logger.error(
                f"ProductAssignment not found for product: {product}, process: {process}"
            )
            return None

    def _validate_product_and_process_consistency(self) -> Tuple[bool, str]:
        """
        Ensures all records in `file_data` have consistent product and process values.

        Checks that every record has the same product and process as the first record to maintain data integrity.
        Returns an error message if inconsistencies are found.

        Args:
            None: Uses `self.file_data` from the inherited `Utils` class.

        Returns:
            Tuple[bool, str]: A tuple containing:
                - `bool`: `True` if all records are consistent, `False` otherwise.
                - `str`: Empty string if valid, error message if inconsistent.

        Side Effects:
            - Logs error messages for any inconsistencies in product or process values.
        """
        if not self.file_data:
            return False, "No data provided in Excel file"

        first_product: str = self.file_data[0].get(
            CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.value
        )
        first_process: str = self.file_data[0].get(
            CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.value
        )
        for idx, record in enumerate(self.file_data):
            if (
                record.get(
                    CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.value
                )
                != first_product
            ):
                return (
                    False,
                    f"Inconsistent product at row {idx + 1}: expected {first_product}, got {record.get(CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.value)}",
                )
            if (
                record.get(
                    CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.value
                )
                != first_process
            ):
                return (
                    False,
                    f"Inconsistent process at row {idx + 1}: expected {first_process}, got {record.get(CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.value)}",
                )
        return True, ""

    def update_allocation_file_cases_details(self) -> List[Dict[str, Any]]:
        """
        Processes and updates case management data from `file_data` with validation and error handling.

        Validates each record's fields against their expected types, updates `CaseManagementCaseModel` instances,
        applies risk details, and tracks errors for error file generation. Uses bulk database operations to
        optimize performance and includes risk-related fields in updates. Maintains product and process consistency.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing records with their error fields, if any.

        Side Effects:
            - Initializes `self.validated_data` and `self.error_data` lists for tracking valid and errored records.
            - Updates `CaseManagementCaseModel` instances in the database using `bulk_update`.
            - Logs minimal information about processing steps and errors for debugging.
        """
        error_record_data: List[Dict[str, Any]] = []
        self.validated_data: List[Dict[str, Any]] = []
        self.error_data: List[Dict[str, Any]] = []

        # Validate product and process consistency across all records
        is_valid: bool
        error_msg: str
        is_valid, error_msg = self._validate_product_and_process_consistency()
        if not is_valid:
            error_record_data: List[Dict[str, Any]] = [
                {"error_fields": error_msg} for _ in self.file_data
            ]
            return error_record_data

        # Extract product and process IDs from the first record
        self.product_id: str = self.file_data[0].get(
            CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.name
        )
        self.process_id: str = self.file_data[0].get(
            CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.name
        )

        # Precompute required fields for validation
        required_fields: set[str] = {
            get_enum_key_with_value(CustomAllocationFileTemplateReservedFieldsEnum, i)
            for i in self.template_required_header_data
            if get_enum_key_with_value(
                CustomAllocationFileTemplateReservedFieldsEnum, i
            )
        }

        # Fetch case instances in bulk for efficiency
        loan_account_numbers: List[str] = [
            self._extract_loan_account_number(record)
            for record in self.file_data
            if self._extract_loan_account_number(record)
        ]
        case_instances: Dict[str, CaseManagementCaseModel] = {
            case.loan_account_number: case
            for case in self.case_management_queryset.filter(
                allocation_file=self.allocation_file_instance,
                loan_account_number__in=loan_account_numbers,
            )
        }
        cases_to_update: List[CaseManagementCaseModel] = []

        for record_idx, record in enumerate(self.file_data):
            error_fields: List[str] = []

            loan_account_number: Optional[str] = self._extract_loan_account_number(
                record
            )
            if not loan_account_number:
                error_fields.append("loan_account_number: Missing")
                error_record_data.append(
                    {"record": record, "error_fields": ", ".join(error_fields)}
                )
                self.error_data.append({"record": record, "error_fields": error_fields})
                continue

            case_instance: Optional[CaseManagementCaseModel] = case_instances.get(
                loan_account_number
            )
            if not case_instance:
                error_fields.append(
                    f"loan_account_number: Case not found for {loan_account_number}"
                )
                error_record_data.append(
                    {"record": record, "error_fields": ", ".join(error_fields)}
                )
                self.error_data.append({"record": record, "error_fields": error_fields})
                continue

            # Validate record fields and store valid values
            validated_record: Dict[str, Any] = {}
            self._validate_case_fields(record, validated_record, error_fields)

            # Apply validated field values to the case instance
            for key, value in validated_record.items():
                setattr(case_instance, key, value)

            # Compute and apply risk details (e.g., risk, risk_points)
            risk_details: Dict[str, Any] = calculate_risk_enum_for_case_instance(
                case_instance
            )
            for key, value in risk_details.items():
                setattr(case_instance, key, value)

            # Identify missing required fields for status determination
            missing_fields: List[str] = [
                f for f in required_fields if f in error_fields
            ]
            if not missing_fields:
                case_instance.field_mapping_status = (
                    CaseManagementFieldStatusEnumChoices.SAVED.value
                )
                case_instance.field_mapping_error_message = None
                self.validated_data.append(validated_record)
            else:
                case_instance.field_mapping_status = (
                    CaseManagementFieldStatusEnumChoices.ERROR.value
                )
                case_instance.missing_required_error_message = ", ".join(missing_fields)
                case_instance.field_mapping_error_message = "; ".join(error_fields)
                self.error_data.append(
                    {**record, "ERROR_FIELDS": ", ".join(error_fields)}
                )
                error_record_data.append(
                    {**record, "ERROR_FIELDS": ", ".join(missing_fields)}
                )

            cases_to_update.append(case_instance)

        # Perform bulk update of case instances, including risk fields
        if cases_to_update:
            update_fields: List[str] = [
                field
                for field in self.field_type_mapping.keys()
                if hasattr(CaseManagementCaseModel, field)
            ] + [
                "field_mapping_status",
                "field_mapping_error_message",
                "missing_required_error_message",
                "risk",
                "risk_points",
            ]
            CaseManagementCaseModel.objects.bulk_update(
                cases_to_update, fields=update_fields
            )

        return error_record_data

    def _extract_loan_account_number(self, record: Dict[str, Any]) -> Optional[str]:
        """
        Extracts the loan account number from a given record.

        Retrieves the loan account number using the enum key defined in `CustomAllocationFileTemplateReservedFieldsEnum`.

        Args:
            record (Dict[str, Any]): The data record containing field-value pairs.

        Returns:
            Optional[str]: The loan account number if present in the record, else `None`.
        """
        return record.get(
            CustomAllocationFileTemplateReservedFieldsEnum.LOAN_ACCOUNT_NUMBER.name
        )

    def _validate_case_fields(
        self,
        record: Dict[str, Any],
        validated_record: Dict[str, Any],
        error_fields: List[str],
    ) -> None:
        """
        Validates fields in a record against their expected types and constraints.

        Iterates through each field in the record, validates its value using `_validate_single_field`,
        and stores valid values in `validated_record`. Invalid fields are recorded in `error_fields`.

        Args:
            record (Dict[str, Any]): The data record containing field-value pairs to validate.
            validated_record (Dict[str, Any]): Dictionary to store validated field names and values.
            error_fields (List[str]): List to append error messages for invalid fields.

        Side Effects:
            - Populates `validated_record` with valid field values.
            - Appends error messages to `error_fields` for invalid fields.
        """
        for field, value in record.items():
            if field in (
                CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.value,
                CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.value,
            ):
                continue
            db_field: Optional[str] = get_enum_value_with_key(
                enum_class=CustomAllocationFileTemplateReservedFieldsEnum, key=field
            )
            if db_field in self.field_type_mapping:
                is_valid: bool
                converted_value: Any
                is_valid, converted_value = self._validate_single_field(
                    db_field, value, *self.field_type_mapping[db_field]
                )
                if is_valid and converted_value is not None:
                    validated_record[db_field] = converted_value
                else:
                    self.set_error(
                        key=field,
                        value=value,
                        error_fields=error_fields,
                        exception=f"Invalid format for {field}",
                    )

    def _validate_single_field(
        self,
        field_name: str,
        value: Any,
        expected_type: Type,
        constraints: Dict[str, Any],
    ) -> Tuple[bool, Any]:
        """
        Validates a single field value against its expected type and constraints.

        Handles various field types (e.g., string, integer, decimal, date, model instances) and applies
        constraints such as max length, email/phone validation, or decimal precision. Returns the validated
        value or `None` if invalid, along with a boolean indicating validity.

        Args:
            field_name (str): The name of the field being validated.
            value (Any): The raw value to validate.
            expected_type (Type): The expected Python type for the field (e.g., str, int, Decimal).
            constraints (Dict[str, Any]): Validation constraints (e.g., max_length, is_email, return_instance).

        Returns:
            Tuple[bool, Any]: A tuple containing:
                - `bool`: `True` if the value is valid, `False` otherwise.
                - `Any`: The converted value or model instance if valid, `None` otherwise.
        """
        if value is None or value == "":
            return True, None

        try:
            converted_value: Any = value
            if expected_type == str:
                str_value: str = str(value)
                if (
                    "max_length" in constraints
                    and len(str_value) > constraints["max_length"]
                ):
                    return False, None
                if "is_email" in constraints and constraints["is_email"]:
                    if not constraints["validation_method"](str_value):
                        return False, None
                if "is_phone_number" in constraints and constraints["is_phone_number"]:
                    str_value: str = str(int(float(str_value)))
                if "validation_method" in constraints and not constraints[
                    "validation_method"
                ](str_value):
                    return False, None
                converted_value: str = str_value
            elif expected_type == int:
                converted_value: int = int(value)
            elif expected_type == Decimal:
                converted_value: Decimal = Decimal(str(value))
                if "max_digits" in constraints and "decimal_places" in constraints:
                    integer_part_len: int = len(
                        str(converted_value).split(".")[0].replace("-", "")
                    )
                    if integer_part_len > (
                        constraints["max_digits"] - constraints["decimal_places"]
                    ):
                        return False, None
                    decimal_part: str = (
                        str(converted_value).split(".")[1]
                        if "." in str(converted_value)
                        else ""
                    )
                    if len(decimal_part) > constraints["decimal_places"]:
                        return False, None
            elif expected_type == datetime.date:
                if isinstance(value, str):
                    try:
                        converted_value: datetime.date = datetime.datetime.strptime(
                            value, "%Y-%m-%d"
                        ).date()
                        return True, converted_value
                    except ValueError:
                        for fmt in ["%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y", "%m-%d-%Y"]:
                            try:
                                converted_value: datetime.date = (
                                    datetime.datetime.strptime(value, fmt).date()
                                )
                                return True, converted_value
                            except ValueError:
                                continue
                        return False, None
                elif isinstance(value, datetime.date):
                    converted_value: datetime.date = value
                else:
                    return False, None
            elif "return_instance" in constraints:
                try:
                    instance: Any = constraints["return_instance"](
                        value, **constraints["kwargs"]
                    )
                    return True, instance
                except ObjectDoesNotExist:
                    return False, None
            else:
                return False, None

            return True, converted_value
        except (ValueError, TypeError, DecimalException):
            return False, None


# class UpdateAllocationFileCaseDetails(Utils):
#     """
#     Handles updating case management details with validation and error tracking.

#     Validates fields against model types, updates case instances, and tracks errors for error file generation.
#     Processes records from file_data, ensuring consistency in product and process, and updates case statuses.
#     Optimized for performance using bulk database operations and streamlined validation, without caching or constructor modifications.
#     """

#     def _get_product_assignment_instance(
#         self, product: str, process: str
#     ) -> Optional[LoanConfigurationsProductAssignmentModel]:
#         """
#         Retrieves a ProductAssignment instance based on product and process titles.

#         Args:
#             product (str): The title of the product.
#             process (str): The title of the process.

#         Returns:
#             Optional[LoanConfigurationsProductAssignmentModel]: The ProductAssignment instance if found, None otherwise.

#         Side Effects:
#             - Sets self.product_instance and self.process_instance if found.
#             - Logs an error if the product, process, or assignment is not found.
#         """
#         try:
#             self.product_instance: LoanConfigurationsProductsModel = (
#                 LoanConfigurationsProductsModel.objects.get(title=product)
#             )
#             self.process_instance: LoanConfigurationsProcessModel = (
#                 LoanConfigurationsProcessModel.objects.get(title=process)
#             )
#             return LoanConfigurationsProductAssignmentModel.objects.get(
#                 product=self.product_instance, process=self.process_instance
#             )
#         except ObjectDoesNotExist:
#             self.logger.error(
#                 f"ProductAssignment not found for product: {product}, process: {process}"
#             )
#             return None

#     def _validate_product_and_process_consistency(self) -> Tuple[bool, str]:
#         """
#         Validates that all rows in file_data have the same product and process values.

#         Args:
#             None (uses self.file_data)

#         Returns:
#             Tuple[bool, str]: (is_valid, error_message)

#         Side Effects:
#             - Logs errors for inconsistent product or process values.
#         """
#         if not self.file_data:
#             return False, "No data provided in Excel file"

#         first_product = self.file_data[0].get(
#             CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.value
#         )
#         first_process = self.file_data[0].get(
#             CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.value
#         )
#         for idx, record in enumerate(self.file_data):
#             if (
#                 record.get(
#                     CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.value
#                 )
#                 != first_product
#             ):
#                 return (
#                     False,
#                     f"Inconsistent product at row {idx + 1}: expected {first_product}, got {record.get(CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.value)}",
#                 )
#             if (
#                 record.get(
#                     CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.value
#                 )
#                 != first_process
#             ):
#                 return (
#                     False,
#                     f"Inconsistent process at row {idx + 1}: expected {first_process}, got {record.get(CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.value)}",
#                 )
#         return True, ""

#     def update_allocation_file_cases_details(self) -> List[Dict[str, Any]]:
#         """
#         Validates and updates case management data from file_data.

#         Processes records, validates fields, updates case statuses, and tracks errors.
#         Uses bulk database operations for performance, without caching or constructor modifications.

#         Returns:
#             List[Dict[str, Any]]: Error records with their error fields.

#         Side Effects:
#             - Initializes validated_data and error_data lists.
#             - Updates case instances in the database using bulk_update.
#             - Logs minimal processing steps and errors.
#         """
#         error_record_data: List[Dict[str, Any]] = []
#         self.validated_data: List[Dict[str, Any]] = []
#         self.error_data: List[Dict[str, Any]] = []

#         # Validate product and process consistency
#         is_valid, error_msg = self._validate_product_and_process_consistency()
#         if not is_valid:
#             error_record_data = [{"error_fields": error_msg} for _ in self.file_data]
#             return error_record_data

#         # Get product and process IDs
#         self.product_id = self.file_data[0].get(
#             CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.name
#         )
#         self.process_id = self.file_data[0].get(
#             CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.name
#         )

#         # Precompute required fields
#         required_fields = {
#             get_enum_key_with_value(CustomAllocationFileTemplateReservedFieldsEnum, i)
#             for i in self.template_required_header_data
#             if get_enum_key_with_value(
#                 CustomAllocationFileTemplateReservedFieldsEnum, i
#             )
#         }

#         # Bulk fetch case instances
#         loan_account_numbers = [
#             self._extract_loan_account_number(record)
#             for record in self.file_data
#             if self._extract_loan_account_number(record)
#         ]
#         case_instances = {
#             case.loan_account_number: case
#             for case in self.case_management_queryset.filter(
#                 allocation_file=self.allocation_file_instance,
#                 loan_account_number__in=loan_account_numbers,
#             )
#         }
#         cases_to_update = []

#         for record_idx, record in enumerate(self.file_data):
#             error_fields: List[str] = []

#             loan_account_number = self._extract_loan_account_number(record)
#             if not loan_account_number:
#                 error_fields.append("loan_account_number: Missing")
#                 error_record_data.append(
#                     {"record": record, "error_fields": ", ".join(error_fields)}
#                 )
#                 self.error_data.append({"record": record, "error_fields": error_fields})
#                 continue

#             case_instance = case_instances.get(loan_account_number)
#             if not case_instance:
#                 error_fields.append(
#                     f"loan_account_number: Case not found for {loan_account_number}"
#                 )
#                 error_record_data.append(
#                     {"record": record, "error_fields": ", ".join(error_fields)}
#                 )
#                 self.error_data.append({"record": record, "error_fields": error_fields})
#                 continue

#             # Validate fields
#             validated_record: Dict[str, Any] = {}
#             self._validate_case_fields(record, validated_record, error_fields)

#             # Apply validated fields
#             for key, value in validated_record.items():
#                 setattr(case_instance, key, value)

#             # Update risk details
#             risk_details = calculate_risk_enum_for_case_instance(case_instance)
#             print('risk_details',risk_details)
#             for key, value in risk_details.items():
#                 setattr(case_instance, key, value)

#             # Check for missing required fields
#             missing_fields = [f for f in required_fields if f in error_fields]
#             if not missing_fields:
#                 case_instance.field_mapping_status = (
#                     CaseManagementFieldStatusEnumChoices.SAVED.value
#                 )
#                 case_instance.field_mapping_error_message = None
#                 self.validated_data.append(validated_record)
#             else:
#                 case_instance.field_mapping_status = (
#                     CaseManagementFieldStatusEnumChoices.ERROR.value
#                 )
#                 case_instance.missing_required_error_message = ", ".join(missing_fields)
#                 case_instance.field_mapping_error_message = "; ".join(error_fields)
#                 self.error_data.append(
#                     {"record": record, "error_fields": ", ".join(error_fields)}
#                 )
#                 error_record_data.append(
#                     {"record": record, "error_fields": ", ".join(missing_fields)}
#                 )

#             cases_to_update.append(case_instance)

#         # Bulk update case instances
#         if cases_to_update:
#             update_fields = [
#                 field
#                 for field in self.field_type_mapping.keys()
#                 if hasattr(CaseManagementCaseModel, field)
#             ] + [
#                 "field_mapping_status",
#                 "field_mapping_error_message",
#                 "missing_required_error_message",
#                 "risk_details"
#             ]
#             CaseManagementCaseModel.objects.bulk_update(
#                 cases_to_update, fields=update_fields
#             )

#         return error_record_data

#     def _extract_loan_account_number(self, record: Dict[str, Any]) -> Optional[str]:
#         """
#         Extracts the loan account number from a record.

#         Args:
#             record (Dict[str, Any]): The data record containing field values.

#         Returns:
#             Optional[str]: The loan account number if present, None otherwise.
#         """
#         return record.get(
#             CustomAllocationFileTemplateReservedFieldsEnum.LOAN_ACCOUNT_NUMBER.name
#         )

#     def _validate_case_fields(
#         self,
#         record: Dict[str, Any],
#         validated_record: Dict[str, Any],
#         error_fields: List[str],
#     ) -> None:
#         """
#         Validates case management fields against their expected types and constraints.

#         Args:
#             record (Dict[str, Any]): The data record containing field-value pairs.
#             validated_record (Dict[str, Any]): Dictionary to store validated field values.
#             error_fields (List[str]): List to append error messages for invalid fields.

#         Side Effects:
#             - Populates validated_record with valid field values.
#             - Appends error messages to error_fields for invalid fields.
#         """
#         for field, value in record.items():
#             if field in (
#                 CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.value,
#                 CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.value,
#             ):
#                 continue
#             db_field = get_enum_value_with_key(
#                 enum_class=CustomAllocationFileTemplateReservedFieldsEnum, key=field
#             )
#             if db_field in self.field_type_mapping:
#                 is_valid, converted_value = self._validate_single_field(
#                     db_field, value, *self.field_type_mapping[db_field]
#                 )
#                 if is_valid and converted_value is not None:
#                     validated_record[db_field] = converted_value
#                 else:
#                     self.set_error(
#                         key=field,
#                         value=value,
#                         error_fields=error_fields,
#                         exception=f"Invalid format for {field}",
#                     )

#     def _validate_single_field(
#         self,
#         field_name: str,
#         value: Any,
#         expected_type: Type,
#         constraints: Dict[str, Any],
#     ) -> Tuple[bool, Any]:
#         """
#         Validates a single field value against its expected type and constraints.

#         Args:
#             field_name (str): The name of the field being validated.
#             value (Any): The value to validate.
#             expected_type (Type): The expected Python type for the field.
#             constraints (Dict[str, Any]): Validation constraints (e.g., max_length, is_email).

#         Returns:
#             Tuple[bool, Any]: (is_valid, converted_value or instance or None)
#         """
#         if value is None or value == "":
#             return True, None

#         try:
#             converted_value = value
#             if expected_type == str:
#                 str_value = str(value)
#                 if (
#                     "max_length" in constraints
#                     and len(str_value) > constraints["max_length"]
#                 ):
#                     return False, None
#                 if "is_email" in constraints and constraints["is_email"]:
#                     if not constraints["validation_method"](str_value):
#                         return False, None
#                 if "is_phone_number" in constraints and constraints["is_phone_number"]:
#                     converted_value = str(int(float(str_value)))
#                     str_value = str(int(float(str_value)))

#                 if "validation_method" in constraints and not constraints[
#                     "validation_method"
#                 ](str_value):
#                     return False, None
#                 converted_value = str_value
#             elif expected_type == int:
#                 converted_value = int(value)
#             elif expected_type == Decimal:
#                 converted_value = Decimal(str(value))
#                 if "max_digits" in constraints and "decimal_places" in constraints:
#                     integer_part_len = len(
#                         str(converted_value).split(".")[0].replace("-", "")
#                     )
#                     if integer_part_len > (
#                         constraints["max_digits"] - constraints["decimal_places"]
#                     ):
#                         return False, None
#                     decimal_part = (
#                         str(converted_value).split(".")[1]
#                         if "." in str(converted_value)
#                         else ""
#                     )
#                     if len(decimal_part) > constraints["decimal_places"]:
#                         return False, None
#             elif expected_type == datetime.date:
#                 if isinstance(value, str):
#                     try:
#                         converted_value = datetime.datetime.strptime(
#                             value, "%Y-%m-%d"
#                         ).date()
#                         return True, converted_value
#                     except ValueError:
#                         for fmt in ["%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y", "%m-%d-%Y"]:
#                             try:
#                                 converted_value = datetime.datetime.strptime(
#                                     value, fmt
#                                 ).date()
#                                 return True, converted_value
#                             except ValueError:
#                                 continue
#                         return False, None
#                 elif isinstance(value, datetime.date):
#                     converted_value = value
#                 else:
#                     return False, None
#             elif "return_instance" in constraints:
#                 try:
#                     instance = constraints["return_instance"](
#                         value, **constraints["kwargs"]
#                     )
#                     return True, instance
#                 except ObjectDoesNotExist:
#                     return False, None
#             else:
#                 return False, None

#             return True, converted_value
#         except (ValueError, TypeError, DecimalException):
#             return False, None


# class UpdateAllocationFileCaseDetails(Utils):
#     """
#     Handles updating case management details with validation and error tracking.

#     Validates fields against model types, updates case instances, and tracks errors for error file generation.
#     Processes records from file_data, ensuring consistency in product and process, and updates case statuses.
#     """

#     def _get_product_assignment_instance(
#         self, product: str, process: str
#     ) -> Optional[LoanConfigurationsProductAssignmentModel]:
#         """
#         Retrieves a ProductAssignment instance based on product and process titles.

#         Args:
#             product (str): The title of the product.
#             process (str): The title of the process.

#         Returns:
#             Optional[LoanConfigurationsProductAssignmentModel]: The ProductAssignment instance if found, None otherwise.

#         Side Effects:
#             - Sets self.product_instance and self.process_instance if found.
#             - Logs an error if the product, process, or assignment is not found.
#         """
#         try:
#             # Retrieve product and process instances
#             self.product_instance: LoanConfigurationsProductsModel = (
#                 LoanConfigurationsProductsModel.objects.get(title=product)
#             )
#             self.process_instance: LoanConfigurationsProcessModel = (
#                 LoanConfigurationsProcessModel.objects.get(title=process)
#             )
#             # Retrieve the ProductAssignment instance
#             return LoanConfigurationsProductAssignmentModel.objects.get(
#                 product=self.product_instance, process=self.process_instance
#             )
#         except ObjectDoesNotExist:
#             self.logger.error(
#                 f"ProductAssignment not found for product: {product}, process: {process}"
#             )
#             return None

#     def _validate_product_and_process_consistency(self) -> Tuple[bool, str]:
#         """
#         Validates that all rows in file_data have the same product and process values.

#         Args:
#             None (uses self.file_data)

#         Returns:
#             Tuple[bool, str]: A tuple containing:
#                 - bool: True if all records have consistent product and process, False otherwise.
#                 - str: Error message if validation fails, empty string if valid.

#         Side Effects:
#             - Logs the start of the validation process.
#             - Logs error messages for inconsistent product or process values.
#         """
#         self.logger.info("_validate_product_and_process_consistency")
#         # Check if file_data is empty
#         if not self.file_data:
#             return False, "No data provided in Excel file"
#         # Get product and process from the first record
#         first_product: str = self.file_data[0].get(
#             CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.value
#         )
#         first_process: str = self.file_data[0].get(
#             CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.value
#         )
#         # Check consistency across all records
#         for idx, record in enumerate(self.file_data):
#             if (
#                 record.get(
#                     CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.value
#                 )
#                 != first_product
#             ):
#                 return (
#                     False,
#                     f"Inconsistent product at row {idx + 1}: expected {first_product}, got {record.get(CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.value)}",
#                 )
#             if (
#                 record.get(
#                     CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.value
#                 )
#                 != first_process
#             ):
#                 return (
#                     False,
#                     f"Inconsistent process at row {idx + 1}: expected {first_process}, got {record.get(CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.value)}",
#                 )
#         return True, ""

#     def update_allocation_file_cases_details(self) -> List[Dict[str, Any]]:
#         """
#         Validates and updates case management data from file_data.

#         Processes each record, validates fields, updates case statuses, and tracks errors for error file generation.
#         Ensures product and process consistency before processing records.

#         Returns:
#             List[Dict[str, Any]]: A list of dictionaries containing error records with their error fields.

#         Side Effects:
#             - Initializes validated_data and error_data lists.
#             - Logs processing steps and errors.
#             - Updates case instances in the database.
#             - Sets field_mapping_status and error messages on case instances.
#         """
#         self.logger.info("Starting update_allocation_file_cases_details process")
#         # Initialize lists for error and validated data
#         error_record_data: Dict[str, str] = []
#         self.validated_data: Dict[str, str] = []
#         self.error_data: Dict[str, str] = []

#         # Validate product and process consistency
#         is_valid, error_msg = self._validate_product_and_process_consistency()
#         if not is_valid:
#             self.logger.error(error_msg)
#             # Return error for all records if validation fails
#             error_record_data: Dict[str, str] = [
#                 {"error_fields": error_msg} for _ in self.file_data
#             ]
#             return error_record_data

#         # Get product and process IDs from the first record
#         self.product_id: str = self.file_data[0].get(
#             CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.name
#         )
#         self.process_id: str = self.file_data[0].get(
#             CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.name
#         )
#         # Note: Commented out lines for product_assignment_instance and allocation_file_instance creation
#         # self.product_assignment_instance = self._get_product_assignment_instance(
#         #     self.product_id, self.process_id
#         # )
#         # self.allocation_file_instance = self._create_allocation_file()

#         # Process each record in file_data
#         for record_idx, record in enumerate(self.file_data):
#             error_fields: List[str] = []
#             self.logger.info(
#                 f"Processing record {record_idx + 1}/{len(self.file_data)}"
#             )

#             # Extract loan account number
#             loan_account_number: str = self._extract_loan_account_number(record)
#             if not loan_account_number:
#                 error_fields.append("loan_account_number: Missing")
#                 error_record_data.append(
#                     {**record, "error_fields": ", ".join(error_fields)}
#                 )
#                 self.error_data.append({"record": record, "error_fields": error_fields})
#                 self.logger.warning(
#                     "Skipping record due to missing loan_account_number"
#                 )
#                 continue

#             try:
#                 # Retrieve case instance for the loan account number
#                 case_instance: CaseManagementCaseModel = (
#                     self.case_management_queryset.get(
#                         allocation_file=self.allocation_file_instance,
#                         loan_account_number=loan_account_number,
#                     )
#                 )
#                 self.logger.info(
#                     f"Retrieved case instance for {loan_account_number}: {case_instance.id}"
#                 )

#                 # Validate fields and store valid data
#                 validated_record: Dict[str, Any] = {}
#                 self._validate_case_fields(record, validated_record, error_fields)
#                 print('record',record)
#                 print(
#                     "validated_record", validated_record
#                 )  # Debug: Output validated record
#                 # Update case instance with validated fields
#                 for validation_record_key in validated_record:
#                     try:
#                         # Set field value and save instance
#                         setattr(
#                             case_instance,
#                             validation_record_key,
#                             validated_record[validation_record_key],
#                         )
#                         case_instance.save()
#                     except Exception as e:
#                         print(
#                             "Exception",
#                             e,
#                             validation_record_key,
#                             validated_record[validation_record_key],
#                         )  # Debug: Log exception details
#                         error_fields.append(validation_record_key)

#                 # Update risk details
#                 risk_details: Dict[str, Any] = calculate_risk_enum_for_case_instance(
#                     case_instance
#                 )
#                 print("risk_details", risk_details)  # Debug: Output risk details
#                 # Apply risk details to case instance
#                 for risk_details_key in risk_details.keys():
#                     try:
#                         setattr(
#                             case_instance,
#                             risk_details_key,
#                             risk_details[risk_details_key],
#                         )
#                         case_instance.save()
#                     except Exception as e:
#                         print(
#                             "Exception",
#                             e,
#                             risk_details_key,
#                             risk_details[risk_details_key],
#                         )  # Debug: Log exception details
#                         error_fields.append(risk_details_key)

#                 self.logger.debug(f"Updated risk details for case {case_instance.pk}")
#                 print(
#                     "self.template_required_header_data",
#                     self.template_required_header_data,
#                     "error_fields",
#                     error_fields,
#                 )  # Debug: Output required headers and errors
#                 # Check for missing required fields
#                 missing_fields: List = []
#                 for i in self.template_required_header_data:
#                     missing_field = get_enum_key_with_value(
#                         CustomAllocationFileTemplateReservedFieldsEnum, i
#                     )
#                     if missing_field is not None and missing_field in error_fields:
#                         missing_fields.append(missing_field)
#                 print("missing_fields", missing_fields)  # Debug: Output missing fields
#                 # Set field_mapping_status based on missing required fields
#                 if not missing_fields:
#                     self.logger.debug(
#                         f"Setting field_mapping_status to SAVED for case {case_instance.id}"
#                     )
#                     case_instance.field_mapping_status = (
#                         CaseManagementFieldStatusEnumChoices.SAVED.value
#                     )
#                     case_instance.field_mapping_error_message = None
#                     self.validated_data.append(validated_record)
#                 else:
#                     self.logger.debug(
#                         f"Setting field_mapping_status to ERROR for case {case_instance.id}"
#                     )
#                     case_instance.field_mapping_status = (
#                         CaseManagementFieldStatusEnumChoices.ERROR.value
#                     )
#                     case_instance.missing_required_error_message = ", ".join(
#                         missing_fields
#                     )
#                     case_instance.field_mapping_error_message = "; ".join(error_fields)
#                     self.error_data.append(
#                         {"record": record, "error_fields": ", ".join(error_fields)}
#                     )
#                     error_record_data.append(
#                         {
#                             **record,
#                             "error_fields": (
#                                 ", ".join(missing_fields) if missing_fields else ""
#                             ),
#                         }
#                     )

#                 # Save the updated case instance
#                 case_instance.save()

#             except CaseManagementCaseModel.DoesNotExist:
#                 # Handle case where no matching case instance is found
#                 error_fields.append(
#                     f"loan_account_number: Case not found for {loan_account_number}"
#                 )
#                 error_record_data.append(
#                     {**record, "ERROR_AND_MISSING_FIELDS": ", ".join(missing_fields)}
#                 )
#                 self.error_data.append(
#                     {"record": record, "missing_fields": missing_fields}
#                 )
#                 self.logger.error(f"Case not found for {loan_account_number}")
#                 continue

#         self.logger.info(
#             f"Completed processing. Validated: {len(self.validated_data)}, Errors: {len(self.error_data)}"
#         )
#         return error_record_data

#     def _extract_loan_account_number(self, record: Dict[str, Any]) -> Optional[str]:
#         """
#         Extracts the loan account number from a record.

#         Args:
#             record (Dict[str, Any]): The data record containing field values.

#         Returns:
#             Optional[str]: The loan account number if present, None otherwise.

#         Side Effects:
#             - Logs the extracted loan account number for debugging.
#         """
#         loan_account_number = record.get(
#             CustomAllocationFileTemplateReservedFieldsEnum.LOAN_ACCOUNT_NUMBER.name
#         )
#         self.logger.debug(f"Extracting loan_account_number: {loan_account_number}")
#         return loan_account_number

#     def _validate_case_fields(
#         self,
#         record: Dict[str, Any],
#         validated_record: Dict[str, Any],
#         error_fields: List[str],
#     ) -> None:
#         """
#         Validates case management fields against their expected types and constraints.

#         Args:
#             record (Dict[str, Any]): The data record containing field-value pairs.
#             validated_record (Dict[str, Any]): Dictionary to store validated field values.
#             error_fields (List[str]): List to append error messages for invalid fields.

#         Side Effects:
#             - Populates validated_record with valid field values.
#             - Appends error messages to error_fields for invalid fields.
#             - Logs validation steps and results.
#         """
#         self.logger.info("Validating case fields")
#         # Iterate through each field in the record
#         for field, value in record.items():
#             # Skip product and process fields as they are not case-specific
#             if field in (
#                 CustomAllocationFileTemplateReservedFieldsEnum.PRODUCT_TYPE.value,
#                 CustomAllocationFileTemplateReservedFieldsEnum.PROCESS_NAME.value,
#             ):
#                 continue
#             # Map field to database field name using enum
#             db_field = get_enum_value_with_key(
#                 enum_class=CustomAllocationFileTemplateReservedFieldsEnum, key=field
#             )
#             self.logger.debug(f"Validating field: {field} with value: {value}")
#             if db_field in self.field_type_mapping:
#                 # Validate the field value
#                 is_valid, converted_value = self._validate_single_field(
#                     db_field, value, *self.field_type_mapping[db_field]
#                 )
#                 if is_valid and converted_value is not None:
#                     # Store valid value in validated_record
#                     validated_record[db_field] = converted_value
#                     self.logger.debug(f"Field {field} validated successfully")
#                 else:
#                     # Log and record validation errors
#                     self.set_error(
#                         key=field,
#                         value=value,
#                         error_fields=error_fields,
#                         exception=f"Invalid format for {field}",
#                     )
#             else:
#                 self.logger.debug(
#                     f"Field {field} -> {db_field} not in field_type_mapping, skipping"
#                 )

#     def _validate_single_field(
#         self,
#         field_name: str,
#         value: Any,
#         expected_type: Type,
#         constraints: Dict[str, Any],
#     ) -> Tuple[bool, Any]:
#         """
#         Validates a single field value against its expected type and constraints.

#         Args:
#             field_name (str): The name of the field being validated.
#             value (Any): The value to validate.
#             expected_type (Type): The expected Python type for the field.
#             constraints (Dict[str, Any]): Validation constraints (e.g., max_length, is_email).

#         Returns:
#             Tuple[bool, Any]: A tuple containing:
#                 - bool: True if the value is valid, False otherwise.
#                 - Any: The converted value or model instance if valid, None otherwise.

#         Side Effects:
#             - Logs validation steps, successes, and failures.
#         """
#         self.logger.debug(
#             f"Validating {field_name}: type={expected_type}, value={value}"
#         )
#         # Allow null or empty string values
#         if value is None or value == "":
#             self.logger.debug(f"Field {field_name} is null/blank, allowing")
#             return True, None

#         try:
#             converted_value: Any = value
#             if expected_type == str:
#                 # Validate string fields
#                 str_value = str(value)
#                 if (
#                     "max_length" in constraints
#                     and len(str_value) > constraints["max_length"]
#                 ):
#                     return False, None
#                 if "is_email" in constraints and constraints["is_email"]:
#                     if not constraints["validation_method"](str_value):
#                         return False, None
#                 if "is_phone_number" in constraints and constraints["is_phone_number"]:
#                     str_value: str = str(int(float(str_value)))
#                 if "validation_method" in constraints and not constraints[
#                     "validation_method"
#                 ](str_value):
#                     return False, None
#                 converted_value: str = str_value
#             elif expected_type == int:
#                 # Convert to integer
#                 converted_value: int = int(value)
#             elif expected_type == Decimal:
#                 # Convert to Decimal and validate constraints
#                 converted_value: Decimal = Decimal(str(value))
#                 if "max_digits" in constraints and "decimal_places" in constraints:
#                     integer_part_len = len(
#                         str(converted_value).split(".")[0].replace("-", "")
#                     )
#                     if integer_part_len > (
#                         constraints["max_digits"] - constraints["decimal_places"]
#                     ):
#                         return False, None
#                     decimal_part = (
#                         str(converted_value).split(".")[1]
#                         if "." in str(converted_value)
#                         else ""
#                     )
#                     if len(decimal_part) > constraints["decimal_places"]:
#                         return False, None
#             elif expected_type == datetime.date:
#                 # Validate and convert date fields
#                 if isinstance(value, str):
#                     possible_formats: List[str] = [
#                         "%Y-%m-%d",
#                         "%d-%m-%Y",
#                         "%d/%m/%Y",
#                         "%m/%d/%Y",
#                         "%m-%d-%Y",
#                     ]
#                     for fmt in possible_formats:
#                         try:
#                             converted_value = datetime.datetime.strptime(
#                                 value, fmt
#                             ).date()
#                             self.logger.debug(
#                                 f"Successfully parsed date {value} with format {fmt}"
#                             )
#                             return True, converted_value
#                         except ValueError:
#                             continue
#                     self.logger.warning(
#                         f"Invalid date format for {field_name}: {value}"
#                     )
#                     return False, None
#                 elif isinstance(value, datetime.date):
#                     converted_value: datetime.date = value
#                 else:
#                     return False, None
#             elif "return_instance" in constraints:
#                 # Retrieve model instance for fields like billing_cycle or pincode
#                 try:
#                     instance: Any = constraints["return_instance"](
#                         value, **constraints["kwargs"]
#                     )
#                     return True, instance
#                 except ObjectDoesNotExist:
#                     self.logger.warning(f"Instance not found for {field_name}: {value}")
#                     return False, None
#             else:
#                 self.logger.warning(
#                     f"Unsupported type for {field_name}: {expected_type}"
#                 )
#                 return False, None

#             self.logger.debug(
#                 f"Successfully validated {field_name} as {type(converted_value)}"
#             )
#             return True, converted_value
#         except (ValueError, TypeError, DecimalException) as e:
#             self.logger.warning(f"Validation error for {field_name}: {str(e)}")
#             return False, None
