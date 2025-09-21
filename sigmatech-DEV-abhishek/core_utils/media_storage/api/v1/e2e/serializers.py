from rest_framework import serializers
from core_utils.media_storage.api.v1.handlers.file_to_url_handler import (
    FileToUrlConversionHandler,
)
from core_utils.media_storage.models import CoreUtilsMediaUrlModel
from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin


class FileToUrlConversionModelSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    file_fields = serializers.ListField(child=serializers.FileField(), required=False)
    file_field = serializers.FileField(required=False)
    file_field_url = serializers.CharField(required=False)
    file_field_urls = serializers.ListField(
        child=serializers.CharField(required=False), required=False
    )
    results = serializers.JSONField(required=False)
    folder_type = serializers.CharField(required=False)
    handler_class = FileToUrlConversionHandler
    queryset = CoreUtilsMediaUrlModel.objects.all()
