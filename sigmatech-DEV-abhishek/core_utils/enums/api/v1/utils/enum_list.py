from typing import Dict
from core_utils.utils.enums import EnumChoices
from store.operations.allocation_files.v1.utils.enums import AllocationStatusEnum
from store.operations.case_management.enums import (
    CaseManagementFieldStatusEnumChoices,
    RiskTypesEnum,
)

PROJECT_CONFIG_ENUM_CLASSES: Dict[str, EnumChoices] = {
    "RiskTypesEnum": RiskTypesEnum,
    "CaseManagementFieldStatusEnumChoices": CaseManagementFieldStatusEnumChoices,
    "AllocationStatusEnum": AllocationStatusEnum,
}
