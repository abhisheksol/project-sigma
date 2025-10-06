from typing import List, Dict

template_required_fields: List[str] = [
    "customer_name",
    "email_id",
    "primary_number",
    "address_1_type",
    "residential_address_1",
    "residential_address_2",
    "residential_address_3",
    "residential_address_4",
    "residential_customer_city",
    "residential_customer_state",
    "residential_pin_code",
    "residential_country",
    "loan_account_number",
    "crn_number",
    "vehicle_number",
    "credit_limit",
    "cash_limit",
    "total_loan_amount",
    "pos_value",
    "emi_amount",
    "minimum_due_amount",
    "loan_disbursement_date",
    "due_date",
    "last_payment_date",
    "last_payment_amount",
    "last_purchase_amount",
    "billing_cycle",
    "current_dpd",
    "bucket",
]
all_possible_categorized_fields: Dict[str, List[str]] = {
    "CUSTOMER_PERSONAL_DETAILS": [
        "customer_name",
        "father_name",
        "customer_dob",
        "customer_personal_email_id",
        "customer_pan_number",
        "primary_number",
        "alternate_number_1",
        "alternate_number_2",
        "alternate_number_3",
        "alternate_number_4",
    ],
    "CUSTOMER_DEMOGRAPHIC_DETAILS": {
        "RESIDENTIAL_ADDRESS": [
            "address_1_type",
            "residential_address_1",
            "residential_address_2",
            "residential_address_3",
            "residential_address_4",
            "residential_customer_city",
            "residential_customer_state",
            "residential_pin_code",
            "residential_country",
        ],
        "OFFICE_EMPLOYER_ADDRESS": [
            "customer_employer_office_name",
            "address_2_type",
            "customer_employer_address_1",
            "customer_employer_address_2",
            "customer_employer_address_3",
            "customer_employer_address_4",
            "customer_office_city",
            "customer_office_state",
            "customer_office_pin_code",
            "customer_office_country",
            "customers_office_email_id",
        ],
        "OTHER_DEMOGRAPHICS": [
            "occupation_type",
            "customer_bank",
        ],
    },
    "LOAN_ACCOUNT_AND_PRODUCT_DETAILS": [
        "loan_account_number",
        "card_number",
        "crn_number",
        "pool_type",
        "vehicle_number",
        "asset_make",
        "tenure",
        "engineno",
        "chassisno",
    ],
    "FINANCIAL_SUMMARY": [
        "credit_limit",
        "cash_limit",
        "total_loan_amount",
        "pos_value",
        "emi_amount",
        "minimum_due_amount",
        "collectable_amount",
        "penalty_amount",
        "late_payment_fee",
        "late_payment_charges",
        "number_of_emi_paid",
    ],
    "LOAN_LIFECYCLE_DATES": [
        "loan_disbursement_date",
        "maturity_date",
        "emi_start_date",
        "due_date",
        "last_payment_date",
        "last_purchase_date",
        "mob",
        "reason_of_bounce_date",
    ],
    "PAYMENT_HISTORY_AND_RISK_PROFILE": [
        "last_payment_amount",
        "last_purchase_amount",
        "billing_cycle",
        "risk_statement",
        "delinquency_string",
        "current_dpd",
        "bucket",
        "allocation_type",
        "nach_status",
        "reason_of_bounce",
    ],
    "REFERENCES": [
        "reference_name_1",
        "reference_contact_number_1",
        "reference_name_2",
        "reference_contact_number_2",
    ],
}


# EXCEL_POSSIBLE_ADDRESS = [
#     "CUSTOMER_NAME",
#     "FATHER_NAME",
#     "CUSTOMER_DOB",
#     "CUSTOMER_PERSONAL_EMAIL_ID",
#     "CUSTOMER_PAN_NUMBER",
#     "PRIMARY_NUMBER",

#     "ALTERNATE_NUMBER_1",
#     "ALTERNATE_NUMBER_2",
#     "ALTERNATE_NUMBER_3",
#     "ALTERNATE_NUMBER_4",

#     "ADDRESS_1_TYPE",
#     "RESIDENTIAL_ADDRESS_1",
#     "RESIDENTIAL_ADDRESS_2",
#     "RESIDENTIAL_ADDRESS_3",
#     "RESIDENTIAL_ADDRESS_4",
#     "RESIDENTIAL_CUSTOMER_CITY",
#     "RESIDENTIAL_CUSTOMER_STATE",
#     "RESIDENTIAL__PIN_CODE",
#     "RESIDENTIAL_COUNTRY",

#     "CUSTOMER_EMPLOYER/OFFICE_NAME",
#     "ADDRESS_2_TYPE",
#     "CUSTOMER_EMPLOYER_ADDRESS_1",
#     "CUSTOMER_EMPLOYER_ADDRESS_2,"
#     "CUSTOMER_EMPLOYER_ADDRESS_3",
#     "CUSTOMER_EMPLOYER_ADDRESS_4"
#     "CUSTOMER_OFFICE_CITY"
# -CUSTOMER_OFFICE_STATE
# -CUSTOMER_OFFICE_PIN_CODE
# -CUSTOMER_OFFICE_COUNTRY
# -CUSTOMERS_OFFICE_EMAIL_ID

# 👷 Other Demographics:
# OCCUPATION_TYPE
# CUSOMER_BANK


# 3. Loan Account & Product Details
# -LOAN_ACCOUNT_NUMBER
# -CARD_NUMBER
# -CRN_NUMBER
# -PRODUCT_TYPE
# -PROCESS_NAME
# -POOL_TYPE
# -VEHICLE_NUMBER
# -ASSET_MAKE
# -TENURE
# -ENGINENO
# -CHASSISNO


# 4. Financial Summary

# -CREDIT_LIMIT
# -CASH_LIMIT
# -TOTAL_LOAN_AMOUNT
# -POS_VALUE
# -EMI_AMOUNT
# -MINIMUM_DUE_AMOUNT
# -COLLECTABLE_AMOUNT
# -PENALTY_AMOUNT
# -LATE_PAYMENT_FEE
# -LATE_PAYMENT_CHARGES
# -NUMBER_OF_EMI_PAID

# 5. Loan Lifecycle Dates

# -LOAN_DISBURSEMENT_DATE
# -MATURITY_DATE
# -EMI_START_DATE
# -DUE_DATE
# -LAST_PAYMENT_DATE
# -LAST_PURCHASE_DATE
# -MOB
# -REASON_OF_BOUNCE_DATE


# 6. Payment History & Risk Profile

# -LAST_PAYMENT_AMOUNT
# -LAST_PURCHASE_AMOUNT
# -BILLING_CYCLE
# -RISK_STATEMENT
# -DELINQUENCY_STRING
# -CURRENT_ DPD
# -BUCKET
# -ALLOCATION_TYPE
# -NACH_STATUS
# -REASON_OF_BOUNCE


# 7. References

# -REFERENCE_NAME_1
# -REFERENCE_CONTACT_NUMBER_1
# -REFERENCE_NAME_2
# -REFERENCE_CONTACT_NUMBER_2
# ]
