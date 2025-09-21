from core_utils.manage_columns.models import (
    CoreUtilsFeaturesModel,
    UserConfigTableFieldsModel,
    UserConfigTableOrderModel,
)
from core_utils.manage_columns.v1.utils.handlers.user_config_table_field_list_handler import (
    UserConfigTableFieldListHandler,
)
from core_utils.manage_columns.v1.utils.handlers.user_config_table_order_handler import (
    UserConfigManageColumnHandler,
)
from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
from rest_framework import serializers


class GenericUserConfigTableOrderSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    table__feature__title = serializers.CharField(required=False)

    results = serializers.JSONField(required=False)
    handler_class = UserConfigTableFieldListHandler
    queryset = UserConfigTableFieldsModel.objects.all()


class GenericUserConfigTableOrderPostSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    feature = serializers.CharField(required=False)
    results = serializers.JSONField(required=False)
    pagination_count = serializers.IntegerField(required=True)

    feature_queryset = CoreUtilsFeaturesModel.objects.filter(is_active=True)
    handler_class = UserConfigManageColumnHandler
    queryset = UserConfigTableOrderModel.objects.all()


class GenericUserConfigTableOrderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserConfigTableFieldsModel
        fields = ["id", "title", "order", "is_active", "table"]
