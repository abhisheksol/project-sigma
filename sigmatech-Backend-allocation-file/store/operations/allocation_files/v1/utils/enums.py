from core_utils.utils.enums import EnumChoices


class AllocationStatusEnum(EnumChoices):
    INPROCESS = "In Progress"
    EXPIRED = "Expired"
    COMPLETED = "Completed"
