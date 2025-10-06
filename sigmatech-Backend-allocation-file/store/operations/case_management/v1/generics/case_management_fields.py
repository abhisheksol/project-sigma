from store.configurations.loan_config.template_config.enums import (
    CustomAllocationFileTemplateReservedFieldsEnum,
)
from core_utils.utils.enums import list_enum_values
from typing import List


def get_case_management_field_list(common_fields: List[str] = []):
    excel_field_names: List[str] = list_enum_values(
        enum_cls=CustomAllocationFileTemplateReservedFieldsEnum,
    )
    exclude_fields: List[str] = [
        "product_id",
        "process_id",
        "residential_pin_code",
        "customer_office_pin_code",
    ]
    return list(
        set(
            [*[i for i in excel_field_names if i not in exclude_fields], *common_fields]
        )
    )
