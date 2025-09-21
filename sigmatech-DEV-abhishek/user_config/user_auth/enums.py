from core_utils.utils.enums import EnumChoices


class UserRoleEnum(EnumChoices):
    FIELD_OFFICER = "FIELD_OFFICER"
    SUPERVISOR = "SUPERVISOR"
    MANAGER = "MANAGER"
    SR_MANAGER = "SR_MANAGER"
    ADMIN = "ADMIN"


class BloodGroupEnum(EnumChoices):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"


class EmergencyContactRelationEnum(EnumChoices):
    FATHER = "Father"
    MOTHER = "Mother"
    SPOUSE = "Spouse"
    BROTHER = "Brother"
    SISTER = "Sister"
    SON = "Son"
    DAUGHTER = "Daughter"
    FRIEND = "Friend"
    GUARDIAN = "Guardian"
    RELATIVE = "Relative"
    OTHER = "Other"
