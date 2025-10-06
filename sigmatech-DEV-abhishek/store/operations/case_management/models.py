import uuid
from django.db import models
from core_utils.utils.generics.generic_models import CoreGenericModel
from store.configurations.loan_config.template_config.enums import SQLDataTypeEnum
from store.configurations.loan_config.template_config.models import (
    ProcessTemplateFieldMappingModel,
)
from store.operations.allocation_files.models import AllocationFileModel
from store.operations.referal_files.models import ReferalFileModel
from store.operations.case_management.enums import (
    CaseLifecycleStageEnum,
    CaseManagementFieldStatusEnumChoices,
    RiskTypesEnum,
)
from store.configurations.loan_config.models import (
    LoanConfigurationsBucketModel,
    LoanConfigurationsMonthlyCycleModel,
)
from store.configurations.region_config.models import (
    RegionConfigurationAreaModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
)


class CaseLifecycleStageModel(CoreGenericModel):
    """
    Model to store lifecycle stages for case management.
    """

    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid1,
        db_column="CASE_LIFE_CYCLE_STAGE_ID",
        editable=False,
    )
    title = models.CharField(
        max_length=255,
        choices=CaseLifecycleStageEnum.choices(),
        db_column="CASE_LIFE_CYCLE_STAGE",
    )

    class Meta:
        db_table = "CASE_LIFE_CYCLE_STAGE_TABLE"
        indexes = [
            models.Index(fields=["title"], name="idx_stage_title"),
        ]

    def __str__(self) -> str:
        return self.title


class CaseLifecycleDispositionModel(CoreGenericModel):
    """
    Model to store disposition types for case management.
    """

    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid1,
        db_column="CASE_LIFE_CYCLE_DISPOSITION_ID",
        editable=False,
    )
    title = models.CharField(
        max_length=255,
        db_column="DISPOSITION",
        unique=True,
    )
    enum = models.CharField(
        max_length=255,
        choices=CaseLifecycleStageEnum.choices(),
        db_column="DISPOSITION_ENUM",
    )
    short_forms = models.CharField(
        max_length=50,
        db_column="DISPOSITION_SHORT_FORM",
    )

    class Meta:
        db_table = "CASE_LIFE_DISPOSITION_TABLE"

    def __str__(self) -> str:
        return self.title


class AddressTypeModel(CoreGenericModel):
    """
    Master table for address types (Home, Office, Billing, Shipping, etc.)
    """

    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid1,
        db_column="ADDRESS_TYPE_ID",
        editable=False,
    )
    title = models.CharField(
        max_length=50,
        unique=True,
        db_column="ADDRESS_TYPE_TITLE",
    )

    class Meta:
        db_table = "ADDRESS_TYPE_TABLE"

    def __str__(self) -> str:
        return self.title


class CaseManagementCaseModel(CoreGenericModel):
    """
    Model to store case management details, including customer information, loan details,
    and lifecycle status. Supports all possible fields for various loan types, with
    mandatory fields validated for template processing.
    """

    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid1,
        db_column="CASE_MANAGEMENT_ID",
        editable=False,
    )
    allocation_file = models.ForeignKey(
        AllocationFileModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseModel_allocation_file",
        db_column="ALLOCATION_FILE_ID",
    )
    referal_file = models.ForeignKey(
        ReferalFileModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseModel_referal_file",
        db_column="REFERAL_FILE_ID",
        null=True,
        blank=True,
    )
    status = models.ForeignKey(
        CaseLifecycleStageModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseModel_status",
        null=True,
        blank=True,
        db_column="STATUS_ID",
    )
    field_mapping_status = models.CharField(
        max_length=100,
        choices=CaseManagementFieldStatusEnumChoices.choices(),
        default=CaseManagementFieldStatusEnumChoices.ERROR.value,
        db_column="FIELD_MAPPING_STATUS",
    )
    field_mapping_error_message = models.CharField(
        max_length=100, db_column="FIELD_MAPPING_ERROR_MESSAGE", null=True, blank=True
    )
    missing_required_error_message = models.CharField(
        max_length=100,
        db_column="MISSING_REQUIRED_ERROR_MESSAGE",
        null=True,
        blank=True,
    )

    risk = models.CharField(
        max_length=32,
        choices=RiskTypesEnum.choices(),
        null=True,
        blank=True,
        db_column="RISK_TYPE",
    )
    risk_points = models.IntegerField(default=0, db_column="RISK_CAL_POINTS")
    billing_cycle = models.ForeignKey(
        LoanConfigurationsMonthlyCycleModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseModel_billing_cycle",
        blank=True,
        null=True,
        db_column="BILLING_CYCLE",
    )
    bucket = models.ForeignKey(
        LoanConfigurationsBucketModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseModel_bucket",
        blank=True,
        null=True,
        db_column="BUCKET_ID",
    )
    bucket_name = models.CharField(
        max_length=255, null=True, blank=True, db_column="BUCKET_NAME"
    )
    # ? this is a ref field just for tracking purpose
    field_mapping = models.ForeignKey(
        ProcessTemplateFieldMappingModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseModel_field_mapping",
        null=True,
        blank=True,
        db_column="TEMPLATE_FIELD_MAPPING_ID",
    )
    # Customer Personal Details
    customer_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="CUSTOMER_NAME",
    )
    father_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="FATHER_NAME",
    )
    customer_dob = models.DateField(
        blank=True,
        null=True,
        db_column="CUSTOMER_DOB",
    )
    customer_personal_email_id = models.EmailField(
        max_length=255,
        blank=True,
        null=True,
        db_column="CUSTOMER_PERSONAL_EMAIL_ID",
    )
    customer_pan_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_column="CUSTOMER_PAN_NUMBER",
    )
    primary_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_column="PRIMARY_NUMBER",
    )
    alternate_number_1 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_column="ALTERNATE_NUMBER_1",
    )
    alternate_number_2 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_column="ALTERNATE_NUMBER_2",
    )
    alternate_number_3 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_column="ALTERNATE_NUMBER_3",
    )
    alternate_number_4 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_column="ALTERNATE_NUMBER_4",
    )

    # Customer Demographic Details (Office/Employer Address)
    customer_employer_office_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="CUSTOMER_EMPLOYER_OFFICE_NAME",
    )

    customers_office_email_id = models.EmailField(
        max_length=255,
        blank=True,
        null=True,
        db_column="CUSTOMERS_OFFICE_EMAIL_ID",
    )
    occupation_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_column="OCCUPATION_TYPE",
    )
    customer_bank = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_column="CUSTOMER_BANK",
    )
    # Loan Account & Product Details
    loan_account_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_column="LOAN_ACCOUNT_NUMBER",
    )
    card_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_column="CARD_NUMBER",
    )
    crn_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_column="CRN_NUMBER",
    )
    pool_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_column="POOL_TYPE",
    )
    vehicle_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_column="VEHICLE_NUMBER",
    )
    asset_make = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_column="ASSET_MAKE",
    )
    tenure = models.IntegerField(
        blank=True,
        null=True,
        db_column="TENURE",
    )
    engineno = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_column="ENGINENO",
    )
    chassisno = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_column="CHASSISNO",
    )
    # Financial Summary
    credit_limit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        db_column="CREDIT_LIMIT",
    )
    cash_limit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        db_column="CASH_LIMIT",
    )
    total_loan_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        db_column="TOTAL_LOAN_AMOUNT",
    )
    pos_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        db_column="POS_VALUE",
    )
    emi_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        db_column="EMI_AMOUNT",
    )
    minimum_due_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        db_column="MINIMUM_DUE_AMOUNT",
    )
    collectable_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        db_column="COLLECTABLE_AMOUNT",
    )
    penalty_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        db_column="PENALTY_AMOUNT",
    )
    late_payment_fee = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        db_column="LATE_PAYMENT_FEE",
    )
    late_payment_charges = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        db_column="LATE_PAYMENT_CHARGES",
    )
    number_of_emi_paid = models.IntegerField(
        blank=True,
        null=True,
        db_column="NUMBER_OF_EMI_PAID",
    )
    # Loan Lifecycle Dates
    loan_disbursement_date = models.DateField(
        blank=True,
        null=True,
        db_column="LOAN_DISBURSEMENT_DATE",
    )
    maturity_date = models.DateField(
        blank=True,
        null=True,
        db_column="MATURITY_DATE",
    )
    emi_start_date = models.DateField(
        blank=True,
        null=True,
        db_column="EMI_START_DATE",
    )
    due_date = models.DateField(
        blank=True,
        null=True,
        db_column="DUE_DATE",
    )
    last_payment_date = models.DateField(
        blank=True,
        null=True,
        db_column="LAST_PAYMENT_DATE",
    )
    last_purchase_date = models.DateField(
        blank=True,
        null=True,
        db_column="LAST_PURCHASE_DATE",
    )
    mob = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_column="MOB",
    )
    reason_of_bounce_date = models.DateField(
        blank=True,
        null=True,
        db_column="REASON_OF_BOUNCE_DATE",
    )
    # Payment History & Risk Profile
    last_payment_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        db_column="LAST_PAYMENT_AMOUNT",
    )
    last_purchase_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        db_column="LAST_PURCHASE_AMOUNT",
    )

    # billing_cycle = models.CharField(
    #     max_length=50,
    #     blank=True,
    #     null=True,
    #     db_column="BILLING_CYCLE",
    # )
    risk_statement = models.TextField(
        blank=True,
        null=True,
        db_column="RISK_STATEMENT",
    )
    delinquency_string = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="DELINQUENCY_STRING",
    )
    current_dpd = models.IntegerField(
        blank=True,
        null=True,
        db_column="CURRENT_DPD",
    )

    allocation_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_column="ALLOCATION_TYPE",
    )
    nach_status = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_column="NACH_STATUS",
    )
    reason_of_bounce = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="REASON_OF_BOUNCE",
    )
    # References

    reference_name_1 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="REFERENCE_NAME_1",
    )
    reference_contact_number_1 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_column="REFERENCE_CONTACT_NUMBER_1",
    )
    reference_name_2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="REFERENCE_NAME_2",
    )
    reference_contact_number_2 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_column="REFERENCE_CONTACT_NUMBER_2",
    )
    # address fields
    address_1_type = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="ADDRESS_1_TYPE",
    )
    residential_address_1 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="RESIDENTIAL_ADDRESS_1",
    )
    residential_address_2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="RESIDENTIAL_ADDRESS_2",
    )
    residential_address_3 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="RESIDENTIAL_ADDRESS_3",
    )
    residential_address_4 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="RESIDENTIAL_ADDRESS_4",
    )

    residential_customer_city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_column="RESIDENTIAL_CUSTOMER_CITY",
    )

    residential_pin_code = models.ForeignKey(
        RegionConfigurationPincodeModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseAddressModel_residential_pin_code",
        blank=True,
        null=True,
        db_column="RESIDENTIAL_PIN_CODE",
    )
    residential_sub_area = models.ForeignKey(
        RegionConfigurationAreaModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseAddressModel_residential_area",
        blank=True,
        null=True,
        db_column="RESIDENTIAL_SUB_AREA_ID",
    )
    residential_customer_state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_column="RESIDENTIAL_CUSTOMER_STATE",
    )
    residential_country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_column="RESIDENTIAL_COUNTRY",
    )
    address_2_type = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="ADDRESS_2_TYPE",
    )
    customer_employer_address_1 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="CUSTOMER_EMPLOYER_ADDRESS_1",
    )
    customer_employer_address_2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="CUSTOMER_EMPLOYER_ADDRESS_2",
    )
    customer_employer_address_3 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="CUSTOMER_EMPLOYER_ADDRESS_3",
    )
    customer_employer_address_4 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="ADDCUSTOMER_EMPLOYER_ADDRESS_4RESS_4",
    )
    customer_office_city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_column="CUSTOMER_OFFICE_CITY",
    )
    
    

    
    customer_sub_area = models.ForeignKey(
        RegionConfigurationAreaModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseAddressModel_customer_sub_area",
        blank=True,
        null=True,
        db_column="CUSTOMER_OFFICE_SUB_AREA_ID",
    )
    customer_office_state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_column="CUSTOMER_OFFICE_STATE",
    )
    customer_office_country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_column="CUSTOMER_OFFICE_COUNTRY",
    )

    class Meta:
        db_table = "CASE_MANAGEMENT_TABLE"
        unique_together = ("loan_account_number", "allocation_file")


class CaseDispositionModel(CoreGenericModel):
    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid1,
        db_column="CASE_DISPOSITION_ID",
        editable=False,
    )
    assigned_case = models.ForeignKey(
        CaseManagementCaseModel,
        on_delete=models.CASCADE,
        related_name="CaseDispositionModel_assigned_case",
        blank=True,
        null=True,
        db_column="ASSIGNED_CASE_ID",
    )

    disposition = models.ForeignKey(
        CaseLifecycleDispositionModel,
        on_delete=models.CASCADE,
        related_name="CaseDispositionModel_disposition",
        null=True,
        blank=True,
        db_column="DISPOSITION_ID",
    )

    class Meta:
        db_table = "CASE_DISPOTITON_TABLE"


class CaseManagementExtraFieldsModel(CoreGenericModel):
    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid1,
        db_column="CASE_MANAGEMENT_CASE_EXTRA_FIELDS_ID",
        editable=False,
    )

    assigned_case = models.ForeignKey(
        CaseManagementCaseModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementExtraFieldsModel_assigned_case",
        blank=True,
        null=True,
        db_column="CASE_MANAGEMENT_ASSIGNED_CASE_ID",
    )
    title = models.CharField(max_length=255, db_column="EXTRA_FIELD_NAME")
    data_type = models.CharField(
        max_length=255,
        choices=SQLDataTypeEnum.choices(),
        null=True,
        blank=True,
        db_column="EXTRA_FIELD_DATA_TYPE",
    )

    class Meta:
        db_table = "CASE_MANAGEMENT_CASE_EXTRA_FIELDS_TABLE"


class CaseManagementExtraFieldDataModel(CoreGenericModel):
    assigned_case = models.ForeignKey(
        CaseManagementCaseModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementExtraFieldDataModel_assigned_case",
        blank=True,
        null=True,
        db_column="CASE_MANAGEMENT_CASE_EXTRA_FIELD_VALUE_ID",
    )
    title = models.OneToOneField(
        CaseManagementExtraFieldsModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementExtraFieldDataModel_title",
        unique=True,
        db_column="CASE_MANAGEMENT_CASE_EXTRA_FIELDS_ID",
    )
    value = models.CharField(
        max_length=1024, null=True, blank=True, db_column="EXTRA_FIELD_DATA"
    )

    class Meta:
        db_table = "CASE_MANAGEMENT_CASE_EXTRA_FIELD_VALUE_TABLE"


class CaseManagementCaseAddressModel(CoreGenericModel):
    assigned_case = models.ForeignKey(
        CaseManagementCaseModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseAddressModel_assigned_case",
        blank=True,
        null=True,
        db_column="CASE_MANAGEMENT_CASE_ADDRESS_ID",
    )
    address_type = models.ForeignKey(
        AddressTypeModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseModel_address_type",
        blank=True,
        null=True,
        db_column="ADDRESS_TYPE_ID",
    )
    address_1 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="ADDRESS_1",
    )
    address_2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="ADDRESS_2",
    )
    address_3 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="ADDRESS_3",
    )
    address_4 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="ADDRESS_4",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_column="CUSTOMER_CITY",
    )
    region_config_city = models.ForeignKey(
        RegionConfigurationCityModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseAddressModel_region_config_city",
        blank=True,
        null=True,
        db_column="REGION_CONFIG_CUSTOMER_CITY",
    )
    pin_code = models.ForeignKey(
        RegionConfigurationPincodeModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseAddressModel_pin_code",
        blank=True,
        null=True,
        db_column="PIN_CODE_ID",
    )
    state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_column="CUSTOMER_STATE",
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_column="COUNTRY",
    )

    class Meta:
        db_table = "CASE_MANAGEMENT_CASE_ADDRESS_TABLE"
