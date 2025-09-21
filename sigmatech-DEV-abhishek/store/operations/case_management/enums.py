from core_utils.utils.enums import EnumChoices


class CaseLifecycleStageEnum(EnumChoices):
    WHATSAPP_ALLOCATION = "WhatsApp Allocation"
    BOT_CALL_ALLOCATION = "Bot Call Allocation"
    TELECALLER_ALLOCATION = "Telecaller Allocation"
    FIELD_OPERATIONS = "Field Operations"


class RiskTypesEnum(EnumChoices):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
