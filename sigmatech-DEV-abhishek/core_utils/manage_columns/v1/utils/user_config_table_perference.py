from core_utils.models import CoreUtilsFeaturesModel
from user_config.models import UserConfigTableOrderModel
from django.contrib.auth.models import AbstractBaseUser
from core.utils.string_to_class import get_keys_of_serializer

from typing import List

TRU_OPERATE_OPERATOR_ROUND_LOG_TABLE_FIELDS = {
    "equipment_id__title": "Equipment",
    "id": "id",
    "image_id": "Images",
    "tag_id__title": "Tag",
    "text_value": "Value",
    "timestamp": "Timestamp",
    "user_inspection_list": "Inspections",
}

TRU_OPERATE_OPERATOR_ROUND_LOGSHEET_LOG_TABLE_FIELDS = {
    "equipment_id__title": "Equipment",
    "id": "id",
    "interval": "Interval",
    "tag_id__description": "Tag",
    "text_value": "Value",
    "timestamp": "Timestamp",
    "user_inspection_list": "Inspections",
}

REPLACE_CONFIGURED_TITLES_ENUMS = {
    "TRU_OPERATE_OPERATOR_ROUND_LOG_TABLE": TRU_OPERATE_OPERATOR_ROUND_LOG_TABLE_FIELDS,
    "TRU_OPERATE_OPERATOR_ROUND_LOGSHEETS_LOG_TABLE": TRU_OPERATE_OPERATOR_ROUND_LOGSHEET_LOG_TABLE_FIELDS,
}


def get_user_preference_title_list(
    user_instance: AbstractBaseUser, feature_instance: CoreUtilsFeaturesModel
) -> list:
    """
    This function takes user and feature instance and
    return current user preffered table order
    """
    if UserConfigTableOrderModel.objects.filter(
        user=user_instance, feature=feature_instance
    ).exists():
        table_order_instance = UserConfigTableOrderModel.objects.get(
            feature=feature_instance, user=user_instance
        )
        table_fields_queryset = (
            table_order_instance.UserPreferenceTableFieldsModel_table.filter(
                is_active=True
            ).order_by("order")
        )
        title_order: List = [i.title for i in table_fields_queryset]

    else:
        title_order = get_keys_of_serializer(feature_instance.serializer)
    return title_order
