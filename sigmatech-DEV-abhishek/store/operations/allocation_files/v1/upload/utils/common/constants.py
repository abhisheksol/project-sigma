ALLOCATION_FILE_IS_REQUIRED_FIELD_ERROR_MESSAGE = "Allocation file is required"
ALLOCATION_ID_IS_REQUIRED_FIELD_ERROR_MESSAGE = "Allocation ID is required"
ALLOCATION_FILE_NAME_IS_REQUIRED_FIELD_ERROR_MESSAGE = "File name is required"

INCORRECT_ALLOCATION_FILE_URL_FORMAT_ERROR_MESSAGE = "Allocation file URL is not valid"
ALLOCATION_FILE_NAME_EXISTS_ERROR_MESSAGE = "Allocation file name already exists"

ALLOCATION_FILE_PROCESS_ID_INCORRECT_ERROR_MESSAGE = (
    "Invalid process ID or the process is inactive"
)
ALLOCATION_FILE_PRODUCT_ID_INCORRECT_ERROR_MESSAGE = (
    "Invalid product ID or the product is inactive"
)
ALLOCATION_FILE_PRODUCT_ASSIGNMENT_INCORRECT_ERROR_MESSAGE = (
    "Process and product assignment not found or inactive"
)
ALLOCATION_FILE_MONTHLY_CYCLE_INCORRECT_ERROR_MESSAGE = (
    "Invalid monthly cycle ID or the monthly cycle is inactive"
)

INCORRECT_TEMPLATE_INACTIVE_FOR_PROCESS_ASSIGNED_PRODUCT_ERROR_MESSAGE = (
    "Template is not configured for the assigned process-product or is inactive"
)
FILE_ACCESS_ERROR_MESSAGE = "Unable to access the file at the provided URL"
FILE_EMPTY_ERROR_MESSAGE = "The file is empty"
UNSUPPORTED_FILE_FORMAT_ERROR_MESSAGE = (
    "Unsupported file format. Only Excel (.xlsx, .xls) or CSV (.csv) are allowed"
)
FILE_READ_ERROR_MESSAGE = "Error while reading the file"
MISSING_REQUIRED_HEADERS_ERROR_MESSAGE = "Required headers are missing in the file"

LOAN_ACCOUNT_NUMBER_REQUIRED_ERROR_MESSAGE = "Loan account number is required"

LOAN_ACCOUNT_NUMBER_MISSING_ERROR_MESSAGE = (
    "Loan account number is missing in the record"
)
LOAN_ACCOUNT_DUPLICATE_NUMBER_ERROR_MESSAGE = (
    "Duplicate loan account number found in the record"
)

MISSING_MULTI_REF_REQUIRED_HEADERS_ERROR_MESSAGE = (
    "Required multi-reference headers are missing in the file"
)
UNEXPECTED_HEADERS_ERROR_MESSAGE = "Unexpected headers found in the file"
HEADER_ORDER_MISMATCH_ERROR_MESSAGE = (
    "Header order does not match the template configuration"
)
DATA_CONVERSION_ERROR_MESSAGE = "Error while converting file data to JSON"
INVALID_DATA_TYPE_ERROR_MESSAGE = "Invalid data type provided for a field"

CRN_NUMBER_IS_A_REQUIRED_FIELD_ERROR_MESSAGE = "CRN number is required"
LOAN_ACCOUNT_NUMBER_DUPLICATE_ERROR_MESSAGE = "Loan account number already exists"

DUPLICATE_FOUND_CRN_NUMBER_ERROR_MESSAGE = "Duplicate CRN number found"

EMPTY_ALLOCATION_FILE_ERROR_MESSAGE = "Allocation file is empty"

ALLOCATION_FILE_API_SUCCESS_MESSAGE = {
    "POST": "Allocation file uploaded successfully",
    "PUT": "Allocation file re-uploaded successfully",
}

INCORRECT_ALLOCATION_FILE_ID_ERROR_MESSAGE = "Invalid allocation file ID"

INCORRECT_OR_MISSING_CRN_ERROR_MESSAGE = (
    "Re-uploaded file must only contain error CRN IDs from the allocation file"
)

EXTRA_HEADERS_RECEIVED_ERROR_MESSAGE = "Extra headers found in the Excel file"

PROCESS_NAME_IS_MISSING_IN_EXCEL_ERROR_MESSAGE = (
    "Process name is missing in the Excel headers"
)
PRODUCT_TYPE_IS_MISSING_IN_EXCEL_ERROR_MESSAGE = (
    "Product type is missing in the Excel headers"
)
MULTIPLE_PROCESS_NAME_EXCEL_ERROR_MESSAGE = (
    "Multiple process names found in the Excel file"
)
MULTIPLE_PRODUCT_TYPE_EXCEL_ERROR_MESSAGE = (
    "Multiple product types found in the Excel file"
)

ALLOCATION_FILE_HAS_NO_ERROR_RECORDS_ERROR_MESSAGE = (
    "Allocation file does not contain any error records"
)
