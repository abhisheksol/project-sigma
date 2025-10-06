from rest_framework import serializers
from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
from store.operations.allocation_files.models import AllocationFileModel
from store.operations.allocation_files.v1.upload.utils.handler.reupload_allocation_file import (
    ReUploadAllocationFileHandler,
)
from store.operations.allocation_files.v1.upload.utils.handler.upload_allocation_file import (
    UploadAllocationFileHandler,
)


class UploadAllocatinFileModelSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    file_url = serializers.URLField()
    file_name = serializers.CharField()
    handler_class = UploadAllocationFileHandler
    queryset = AllocationFileModel.objects.all()


class ReUploadAllocatinFileModelSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    file_url = serializers.URLField()
    allocation_file_id = serializers.CharField()
    handler_class = ReUploadAllocationFileHandler
    queryset = AllocationFileModel.objects.all()
