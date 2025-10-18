USER_MANAGEMENT_EMAIL_ALREADY_EXISTS = "A user with this email address already exists."
USER_MANAGEMENT_LOGIN_ID_ALREADY_EXISTS = "A user with this employee ID already exists."
USER_MANAGEMENT_PHONE_NUMBER_ALREADY_EXISTS = (
    "A user with this phone number already exists."
)
FIELD_REQUIRED_ERROR_MESSAGE = "This field is required."
INCORRECT_REGION_ID_ERROR_MESSAGE = "Invalid region ID provided."
INCORRECT_ZONE_ID_ERROR_MESSAGE = "Invalid zone ID provided."
INCORRECT_CITY_ID_ERROR_MESSAGE = "Invalid city ID provided."
INCORRECT_PINCODE_ID_ERROR_MESSAGE = "Invalid pincode ID provided."
INCORRECT_AREA_ID_ERROR_MESSAGE = "Invalid area ID provided."

USER_ROLE_INCORRECT_ERROR_MESSAGE = "Invalid user role specified."
ADMIN_ROLE_NOT_ALLOWED_ERROR_MESSAGE = "Admin users cannot be created through the API."
REPORTING_USER_HAS_NO_PERMISSION_TO_USER_ROLE_ERROR_MESSAGE = (
    "The reporting manager does not have permission to assign this user role."
)
USER_ROLE_NOT_SUBORDINATE_TO_REPORTING_USER_ROLE_ERROR_MESSAGE = (
    "The selected user role is not a subordinate of the reporting manager’s role."
)
INCORRECT_REPORTS_TO_ID_ERROR_MESSAGE = (
    "Invalid or inactive reporting manager specified."
)
REPORTS_TO_USER_IS_NOT_LOGIN_USER_SUB_ORDINATE = (
    "The selected reporting manager is not a subordinate of your user role."
)
USER_MANAGEMENT_EMAIL_INCORRECT_FORMAT = "Invalid email format"
SR_MANAGER_HAS_NO_REPORTING_MANAGER_ERROR_MESSAGE = (
    "Sr manager can not report to any user"
)
USER_HAS_REPORTING_USERS_ERROR_MESSAGE = (
    "Cannot update user role because the user has reporting users associated."
)


REUSER_ASSIGNMENT_SUCCESS_MESSAGE = {"PUT": "User reassigned successfully"}

USER_HAS_REPORTING_USERS_DYNAMIC_ERROR_MESSAGE = {
    "reports_to": "Cannot update reports to because the user has reporting users associated.",
    "region_id": "Cannot update region because the user has reporting users associated.",
    "zone_id": "Cannot update zone because the user has reporting users associated.",
    "city_id": "Cannot update city because the user has reporting users associated.",
    "pincode_id": "Cannot update pincode because the user has reporting users associated.",
    "area_id": "Cannot update area because the user has reporting users associated.",
    "status": "Cannot update status because the user has reporting users associated.",
}

INVALID_PRODUCT_ASSIGNMENT_ERROR_MESSAGE = (
    "Product is not assigned to reporting user or invalid product"
)


INVALID_PRODUCT_ASSIGNMENT_ERROR_KEY = "product_assignment_id"


INVALID_PRODUCT_UNASSIGNMENT_ERROR_KEY = "product_unassignment_id"

INVALID_PRODUCT_UNASSIGNMENT_ERROR_MESSAGE = (
    "Cannot unassign product because a subordinate has it assigned"
)
