from core_utils.utils.enums import EnumChoices


class CustomAllocationMultiReferenceFieldValueTypeEnum(EnumChoices):
    BINNARY = "BINNARY"  # 0,0
    TF = "T/F"
    BOOLEAN = "True/False"


class CustomAllocatinFileTemplateStatusEnum(EnumChoices):
    DRAFT = "draft"
    SUBMITTED = "SUBMITTED"


class CustomAllocatinFileTemplateFieldStatusEnum(EnumChoices):
    MAPPED = "MAPPED"
    UNMAPPED = "UNMAPPED"


class DateFormatEnum(EnumChoices):
    """
    Enum for supported date string formats.
    """

    ISO_DATE = "%Y-%m-%d"  # 2025-09-04
    EU_DATE = "%d/%m/%Y"  # 04/09/2025
    US_DATE = "%m/%d/%Y"  # 09/04/2025
    SQL_DATE = "%Y-%m-%d"  # Same as ISO, DB-friendly


class DateTimeFormatEnum(EnumChoices):
    """
    Enum for supported datetime string formats.
    """

    ISO_DATETIME = "%Y-%m-%d %H:%M:%S"  # 2025-09-04 14:23:45
    ISO_DATETIME_MS = "%Y-%m-%d %H:%M:%S.%f"  # 2025-09-04 14:23:45.123456
    ISO_FULL = "%Y-%m-%dT%H:%M:%S%z"  # 2025-09-04T14:23:45+0530
    EU_DATETIME = "%d/%m/%Y %H:%M"  # 04/09/2025 14:23
    US_DATETIME = "%m/%d/%Y %I:%M %p"  # 09/04/2025 02:23 PM
    SQL_DATETIME = "%Y-%m-%d %H:%M:%S"  # DB standard


class DurationFormatEnum(EnumChoices):
    """
    Enum for supported duration/interval formats.
    """

    SECONDS = "%S"  # 45 (seconds only)
    MINUTES_SECONDS = "%M:%S"  # 05:45
    HOURS_MINUTES = "%H:%M"  # 14:23
    HOURS_MINUTES_SECONDS = "%H:%M:%S"  # 14:23:45
    DAYS_HOURS = "%d %H:%M"  # 3 14:23 (3 days, 14 hours 23 minutes)
    ISO_DURATION = "P[n]DT[n]H[n]M[n]S"  # ISO 8601 duration e.g. P3DT4H30M15S


class SQLDataTypeEnum(EnumChoices):
    """
    Enum for supported SQL field data types.
    Non-relational types only.
    """

    STRING = "string"  # VARCHAR, TEXT
    INTEGER = "integer"  # INT, BIGINT, SMALLINT
    DECIMAL = "decimal"  # DECIMAL, NUMERIC
    FLOAT = "float"  # FLOAT, REAL, DOUBLE
    BOOLEAN = "boolean"  # BIT, BOOL
    DATE = "date"  # DATE
    DATETIME = "datetime"  # DATETIME, TIMESTAMP
    TIME = "time"  # TIME
    EMAIL = "email"  # TIME


class CustomAllocationFileTemplateReservedFieldsEnum(EnumChoices):
    # CUSTOMER_PERSONAL_DETAILS
    CUSTOMER_NAME = "customer_name"
    FATHER_NAME = "father_name"
    CUSTOMER_DOB = "customer_dob"
    CUSTOMER_PERSONAL_EMAIL_ID = "customer_personal_email_id"
    CUSTOMER_PAN_NUMBER = "customer_pan_number"
    PRIMARY_NUMBER = "primary_number"
    ALTERNATE_NUMBER_1 = "alternate_number_1"
    ALTERNATE_NUMBER_2 = "alternate_number_2"
    ALTERNATE_NUMBER_3 = "alternate_number_3"
    ALTERNATE_NUMBER_4 = "alternate_number_4"

    # CUSTOMER_DEMOGRAPHIC_DETAILS → RESIDENTIAL_ADDRESS
    ADDRESS_1_TYPE = "address_1_type"
    RESIDENTIAL_ADDRESS_1 = "residential_address_1"
    RESIDENTIAL_ADDRESS_2 = "residential_address_2"
    RESIDENTIAL_ADDRESS_3 = "residential_address_3"
    RESIDENTIAL_ADDRESS_4 = "residential_address_4"
    RESIDENTIAL_CUSTOMER_CITY = "residential_customer_city"
    RESIDENTIAL_CUSTOMER_STATE = "residential_customer_state"
    RESIDENTIAL_PIN_CODE = "residential_pin_code"
    RESIDENTIAL_COUNTRY = "residential_country"

    # CUSTOMER_DEMOGRAPHIC_DETAILS → OFFICE_EMPLOYER_ADDRESS
    ADDRESS_2_TYPE = "address_2_type"
    CUSTOMER_EMPLOYER = "customer_employer_office_name"
    CUSTOMER_EMPLOYER_ADDRESS_1 = "customer_employer_address_1"
    CUSTOMER_EMPLOYER_ADDRESS_2 = "customer_employer_address_2"
    CUSTOMER_EMPLOYER_ADDRESS_3 = "customer_employer_address_3"
    CUSTOMER_EMPLOYER_ADDRESS_4 = "customer_employer_address_4"
    CUSTOMER_OFFICE_CITY = "customer_office_city"
    CUSTOMER_OFFICE_STATE = "customer_office_state"
    CUSTOMER_OFFICE_PIN_CODE = "customer_office_pin_code"
    CUSTOMER_OFFICE_COUNTRY = "customer_office_country"
    CUSTOMERS_OFFICE_EMAIL_ID = "customers_office_email_id"

    # CUSTOMER_DEMOGRAPHIC_DETAILS → OTHER_DEMOGRAPHICS
    OCCUPATION_TYPE = "occupation_type"
    CUSTOMER_BANK = "customer_bank"

    # LOAN_ACCOUNT_AND_PRODUCT_DETAILS
    LOAN_ACCOUNT_NUMBER = "loan_account_number"
    CARD_NUMBER = "card_number"
    CRN_NUMBER = "crn_number"
    POOL_TYPE = "pool_type"
    VEHICLE_NUMBER = "vehicle_number"
    ASSET_MAKE = "asset_make"
    TENURE = "tenure"
    ENGINENO = "engineno"
    CHASSISNO = "chassisno"

    # FINANCIAL_SUMMARY
    CREDIT_LIMIT = "credit_limit"
    CASH_LIMIT = "cash_limit"
    TOTAL_LOAN_AMOUNT = "total_loan_amount"
    POS_VALUE = "pos_value"
    EMI_AMOUNT = "emi_amount"
    MINIMUM_DUE_AMOUNT = "minimum_due_amount"
    COLLECTABLE_AMOUNT = "collectable_amount"
    PENALTY_AMOUNT = "penalty_amount"
    LATE_PAYMENT_FEE = "late_payment_fee"
    LATE_PAYMENT_CHARGES = "late_payment_charges"
    NUMBER_OF_EMI_PAID = "number_of_emi_paid"

    # LOAN_LIFECYCLE_DATES
    LOAN_DISBURSEMENT_DATE = "loan_disbursement_date"
    MATURITY_DATE = "maturity_date"
    EMI_START_DATE = "emi_start_date"
    DUE_DATE = "due_date"
    LAST_PAYMENT_DATE = "last_payment_date"
    LAST_PURCHASE_DATE = "last_purchase_date"
    MOB = "mob"
    REASON_OF_BOUNCE_DATE = "reason_of_bounce_date"

    # PAYMENT_HISTORY_AND_RISK_PROFILE
    LAST_PAYMENT_AMOUNT = "last_payment_amount"
    LAST_PURCHASE_AMOUNT = "last_purchase_amount"
    RISK_STATEMENT = "risk_statement"
    DELINQUENCY_STRING = "delinquency_string"
    CURRENT_DPD = "current_dpd"
    ALLOCATION_TYPE = "allocation_type"
    NACH_STATUS = "nach_status"
    REASON_OF_BOUNCE = "reason_of_bounce"

    # REFERENCES
    REFERENCE_NAME_1 = "reference_name_1"
    REFERENCE_CONTACT_NUMBER_1 = "reference_contact_number_1"
    REFERENCE_NAME_2 = "reference_name_2"
    REFERENCE_CONTACT_NUMBER_2 = "reference_contact_number_2"

    # PROCESS_CONFIG DETAILS
    PROCESS_NAME = "process_id"
    PRODUCT_TYPE = "product_id"
    BILLING_CYCLE = "billing_cycle"
    BUCKET = "bucket"
