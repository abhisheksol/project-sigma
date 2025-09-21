from enum import Enum
from typing import List


class EnumChoices(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


def list_enum_values(enum_cls: Enum) -> List[str]:
    return [e.value for e in enum_cls]


class CoreUtilsStatusEnum(EnumChoices):
    ACTIVATED = "ACTIVATED"
    DEACTIVATED = "DEACTIVATED"


def status_list_enum_values() -> List[str]:
    return list_enum_values(enum_cls=CoreUtilsStatusEnum)


class AccountsApplicationFlowEnum(EnumChoices):
    TRU_OPERATE = "TRU_OPERATE"
    TRU_PLANT = "TRU_PLANT"
    APPLICATION = "APPLICATION"


class AuthOtpTypeEnum(EnumChoices):
    FORGOT_PASSWORD = "FORGOT_PASSWORD"
    SEND_OTP = "SEND_OTP"
    RE_SEND_OTP = "RE_SEND_OTP"


class AccountsGenderEnum(EnumChoices):
    M = "M"
    F = "F"


class APIMethodsEnum(EnumChoices):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
