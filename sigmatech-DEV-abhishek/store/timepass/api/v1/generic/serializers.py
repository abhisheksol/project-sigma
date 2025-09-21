

from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
from rest_framework import serializers
from store.timepass.models import TimepassModel
from store.timepass.api.v1.utils.handlers.time_pass_post_handler import (
    timepassposthandler,
)

class Timepassgetserializer(CoreGenericSerializerMixin,
                            serializers.ModelSerializer):
    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField(source="core_generic_created_at")
    updated_at = serializers.DateTimeField(source="core_generic_updated_at")

    class Meta:
        model = TimepassModel
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
        ]


class Timepasspostserializer(CoreGenericSerializerMixin,
                             serializers.ModelSerializer):
    handler_class = timepassposthandler
    name = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = TimepassModel
        fields = [
            "name",
            "description",
        ]

   