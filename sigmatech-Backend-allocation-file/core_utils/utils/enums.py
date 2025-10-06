from enum import Enum
from typing import List, Optional


class EnumChoices(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


def list_enum_values(enum_cls: Enum) -> List[str]:
    return [e.value for e in enum_cls]


def core_utils_list_enum_keys(enum_cls: Enum) -> List[str]:
    return [e.name for e in enum_cls]


def get_enum_value_with_key(enum_class: Enum, key: str) -> Optional[str]:
    for e in enum_class:

        if str(e.name) == str(key):
            return e.value
    return None


def get_enum_key_with_value(enum_class: Enum, value: str) -> Optional[str]:
    for e in enum_class:

        if str(e.value) == str(value):
            return e.name
    return None


class CoreUtilsStatusEnum(EnumChoices):
    ACTIVATED = "ACTIVATED"
    DEACTIVATED = "DEACTIVATED"


def status_list_enum_values() -> List[str]:
    return list_enum_values(enum_cls=CoreUtilsStatusEnum)


class AuthOtpTypeEnum(EnumChoices):
    FORGOT_PASSWORD = "FORGOT_PASSWORD"
    SEND_OTP = "SEND_OTP"
    RE_SEND_OTP = "RE_SEND_OTP"


class AccountsGenderEnum(EnumChoices):
    M = "M"
    F = "F"


class APIMethodsEnum(EnumChoices):
    GET = "Get"
    POST = "Post"
    PUT = "Put"
    DELETE = "Delete"
