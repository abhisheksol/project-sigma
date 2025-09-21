import uuid
from django.db import models
from core_utils.utils.generics.generic_models import CoreGenericModel
from store.configurations.loan_config.template_config.enums import SQLDataTypeEnum
from store.operations.allocation_files.models import AllocationFileModel
from store.operations.referal_files.models import ReferalFileModel
from store.operations.case_management.enums import (
    CaseLifecycleStageEnum,
    RiskTypesEnum,
)
from store.configurations.loan_config.models import LoanConfigurationsBucketModel
from store.configurations.region_config.models import (
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
        return str(self.title or "")


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
        # indexes = [
        #     models.Index(fields=["title"], name="idx_disposition_title"),
        #     models.Index(fields=["enum"], name="idx_disposition_enum"),
        #     models.Index(fields=["short_forms"], name="idx_disposition_short_forms"),
        # ]

    def __str__(self) -> str:
        return str(self.title or "")


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
        indexes = [
            models.Index(fields=["title"], name="idx_address_type_title"),
        ]

    def __str__(self) -> str:
        return str(self.title or "")


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
    disposition = models.ForeignKey(
        CaseLifecycleDispositionModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseModel_disposition",
        null=True,
        blank=True,
        db_column="DISPOSITION_ID",
    )
    risk = models.CharField(
        max_length=32,
        choices=RiskTypesEnum.choices(),
        null=True,
        blank=True,
        db_column="RISK_TYPE",
    )
    bucket = models.ForeignKey(
        LoanConfigurationsBucketModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseModel_bucket",
        blank=False,
        null=False,
        db_column="BUCKET_ID",
    )
    # Customer Personal Details
    customer_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
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
        blank=False,
        null=False,
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
        blank=False,
        null=False,
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
        unique=True,
        blank=False,
        null=False,
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
        blank=False,
        null=False,
        db_column="CREDIT_LIMIT",
    )
    cash_limit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=False,
        null=False,
        db_column="CASH_LIMIT",
    )
    total_loan_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=False,
        null=False,
        db_column="TOTAL_LOAN_AMOUNT",
    )
    pos_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=False,
        null=False,
        db_column="POS_VALUE",
    )
    emi_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=False,
        null=False,
        db_column="EMI_AMOUNT",
    )
    minimum_due_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=False,
        null=False,
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
        blank=False,
        null=False,
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
        blank=False,
        null=False,
        db_column="DUE_DATE",
    )
    last_payment_date = models.DateField(
        blank=False,
        null=False,
        db_column="LAST_PAYMENT_DATE",
    )
    last_purchase_date = models.DateField(
        blank=True,
        null=True,
        db_column="LAST_PURCHASE_DATE",
    )
    mob = models.IntegerField(
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
        blank=False,
        null=False,
        db_column="LAST_PAYMENT_AMOUNT",
    )
    last_purchase_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=False,
        null=False,
        db_column="LAST_PURCHASE_AMOUNT",
    )
    billing_cycle = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        db_column="BILLING_CYCLE",
    )
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
        blank=False,
        null=False,
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

    class Meta:
        db_table = "CASE_MANAGEMENT_TABLE"
       

class CaseManagementExtraFieldsModel(CoreGenericModel):
    assigned_case = models.ForeignKey(
        CaseManagementCaseModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementExtraFieldsModel_assigned_case",
        blank=False,
        null=False,
        db_column="CASE_MANAGEMENT_CASE_EXTRA_FIELDS_ID",
    )
    title = models.CharField(max_length=255, unique=True, db_column="EXTRA_FIELD_NAME")
    data_type = models.CharField(
        max_length=255,
        choices=SQLDataTypeEnum.choices(),
        null=True,
        blank=True,
        db_column="EXTRA_FIELD_DATA_TYPE",
    )

    class Meta:
        db_table = "CASE_MANAGEMENT_CASE_EXTRA_FIELDS_TABLE"
        # indexes = [
        #     models.Index(
        #         fields=["assigned_case"], name="idx_extra_fields_assigned_case"
        #     ),
        #     models.Index(fields=["title"], name="idx_extra_fields_title_case"),
        # ]


class CaseManagementExtraFieldDataModel(CoreGenericModel):
    assigned_case = models.ForeignKey(
        CaseManagementCaseModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementExtraFieldDataModel_assigned_case",
        blank=False,
        null=False,
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
        # indexes = [
        #     models.Index(fields=["assigned_case"], name="idx_ext_field_data_case"),
        #     models.Index(fields=["title"], name="idx_ext_field_title_case"),
        #     models.Index(fields=["value"], name="idx_ext_field_value_case"),
        # ]


class CaseManagementCaseAddressModel(CoreGenericModel):
    assigned_case = models.ForeignKey(
        CaseManagementCaseModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseAddressModel_assigned_case",
        blank=False,
        null=False,
        db_column="CASE_MANAGEMENT_CASE_ADDRESS_ID",
    )
    address_type = models.ForeignKey(
        AddressTypeModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseModel_address_type",
        blank=False,
        null=False,
        db_column="ADDRESS_TYPE_ID",
    )
    address_1 = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        db_column="ADDRESS_1",
    )
    address_2 = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        db_column="ADDRESS_2",
    )
    address_3 = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        db_column="ADDRESS_3",
    )
    address_4 = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        db_column="ADDRESS_4",
    )
    city = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        db_column="CUSTOMER_CITY",
    )
    region_config_city = models.ForeignKey(
        RegionConfigurationCityModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseAddressModel_region_config_city",
        blank=False,
        null=False,
        db_column="REGION_CONFIG_CUSTOMER_CITY",
    )
    pin_code = models.ForeignKey(
        RegionConfigurationPincodeModel,
        on_delete=models.CASCADE,
        related_name="CaseManagementCaseAddressModel_pin_code",
        blank=False,
        null=False,
        db_column="PIN_CODE_ID",
    )
    state = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        db_column="CUSTOMER_STATE",
    )
    country = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        db_column="COUNTRY",
    )

    class Meta:
        db_table = "CASE_MANAGEMENT_CASE_ADDRESS_TABLE"
