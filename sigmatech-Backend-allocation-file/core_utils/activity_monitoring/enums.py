from core_utils.utils.enums import EnumChoices


class ActivityMonitoringMethodTypeEnumChoices(EnumChoices):
    CREATE = "Created"
    UPDATE = "Updated"
    ACTIVATED = "Activated"
    INACTIVATED = "Inactivated"


class ActivityMonitoringBackGroundActivityEnum(EnumChoices):
    ALLOCATION_FILE = "ALLOCATION_FILE"
    REFERAL_FILE = "REFERAL_FILE"


class ActivityMonitoringBackGroundStatusEnum(EnumChoices):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
