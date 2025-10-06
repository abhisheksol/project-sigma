from rest_framework import serializers

from core_utils.utils.generics.serializers.generic_serializers import (
    CoreGenericHelperAPISerializerMethodField,
)
from store.operations.allocation_files.models import AllocationFileModel
from store.operations.allocation_files.v1.utils.enums import AllocationStatusEnum


class AllocationFileStatusListHelperModelSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()

    @classmethod
    def get_dropdown_data(cls):
        return AllocationStatusEnum.choices()

    def to_representation(self, instance):
        # Handle Enum
        if isinstance(instance, AllocationStatusEnum):
            return {"key": instance.value, "value": instance.value}

        # Handle dict
        elif isinstance(instance, dict):
            return {"key": instance.get("key"), "value": instance.get("value")}

        # Handle tuple like ('DRAFT', 'Draft')
        elif isinstance(instance, tuple) and len(instance) == 2:
            return {"key": instance[0], "value": instance[1]}

        return super().to_representation(instance)


class AllocationFileListHelperModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):
    label = serializers.CharField(source="title")
    value = serializers.CharField(source="id")

    class Meta:
        model = AllocationFileModel
        fields = ["label", "value"]
