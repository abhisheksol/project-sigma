from core_utils.utils.enums import EnumChoices


class CaseLifecycleStageEnum(EnumChoices):
    WHATSAPP_ALLOCATION = "WhatsApp"
    BOT_CALL_ALLOCATION = "Bot Call"
    TELECALLER_ALLOCATION = "Telecaller"
    FIELD_OPERATIONS = "Field Operations"
    FLOW = "Flow"


class RiskTypesEnum(EnumChoices):
    CRITICAL = "CRITICAL".capitalize()
    LOW = "LOW".capitalize()
    MEDIUM = "MEDIUM".capitalize()
    HIGH = "HIGH".capitalize()


class CaseManagementAddressTypeEnumChoices(EnumChoices):
    RESIDENTIAL_ADDRESS = "RESIDENTIAL_ADDRESS"
    COMPANY_ADDRESS = "COMPANY_ADDRESS"


class CaseManagementFieldStatusEnumChoices(EnumChoices):
    SAVED = "Saved"
    ERROR = "Error"
