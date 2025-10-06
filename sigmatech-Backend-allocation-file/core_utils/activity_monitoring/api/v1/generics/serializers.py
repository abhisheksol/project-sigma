from rest_framework import serializers

from core_utils.activity_monitoring.api.v1.generics.utils.handlers.activity_method_enum_helper_list_handler import (
    ActivityMethodEnumHelperListEnumHandler,
)
from core_utils.activity_monitoring.models import (
    ActivityMonitoringLinkedEntityModel,
    ActivityMonitoringLogModel,
    ActivityTypeModel,
)
from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin


class ActivityMonitoringLogListModelSerializer(serializers.ModelSerializer):
    core_generic_created_at__date = serializers.SerializerMethodField()
    core_generic_created_at__time = serializers.SerializerMethodField()
    method = serializers.SerializerMethodField()
    activity_type = serializers.CharField(source="activity_type.lable")
    activity_type__linked_entity__title = serializers.CharField(
        source="activity_type.linked_entity.title"
    )

    class Meta:
        model = ActivityMonitoringLogModel
        fields = [
            "id",
            "activity_type",
            "description",
            "core_generic_created_at__date",
            "core_generic_created_at__time",
            "method",
            "activity_type__linked_entity__title",
        ]

    def get_core_generic_created_at__date(self, obj: ActivityMonitoringLogModel):
        return obj.core_generic_created_at.date()

    def get_core_generic_created_at__time(self, obj: ActivityMonitoringLogModel):
        return obj.core_generic_created_at

    def get_method(self, obj: ActivityMonitoringLogModel):
        return {"method": obj.method.method, "color": obj.method.color}


class ActivityMonitoringLinkedEntityModelSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source="id")
    label = serializers.CharField(source="title")

    class Meta:
        model = ActivityMonitoringLinkedEntityModel
        fields = ["value", "label"]


class ActivityTypeHelperListModelSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source="id")
    label = serializers.CharField(source="lable")

    class Meta:
        model = ActivityTypeModel
        fields = ["value", "label"]


class ActivityMethodEnumHelperListEnumSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    results = serializers.JSONField(required=False)
    handler_class = ActivityMethodEnumHelperListEnumHandler
    queryset = ActivityTypeModel.objects.all()
