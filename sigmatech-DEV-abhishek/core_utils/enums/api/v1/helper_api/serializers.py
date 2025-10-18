from rest_framework import serializers
from core_utils.enums.api.v1.utils.handler import EnumHelperListHandler
from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin


class EnumHelperHelperListSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    enum_class = serializers.CharField()
    results = serializers.JSONField(required=False)
    handler_class = EnumHelperListHandler
