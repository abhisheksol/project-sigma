from datetime import timezone
from rest_framework import serializers
from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
from store.operations.allocation_files.models import AllocationFileModel


class AllocatinFileUploadModelSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    file_url = serializers.URLField()
    file_name = serializers.CharField()
    cycle_id = serializers.CharField()
    product_id = serializers.CharField()
    process_id = serializers.CharField()
    handler_class = None


class AllocationFileListSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):

    product_assignment__process__title = serializers.CharField(
        source="product_assignment.process.title", default=None, allow_blank=True
    )
    product_assignment__product__title = serializers.CharField(
        source="product_assignment.product.title", default=None, allow_blank=True
    )
    logo = serializers.URLField(
        source="product_assignment.process.logo", default=None, allow_blank=True)
    upload_date = serializers.DateTimeField(source="core_generic_created_at")
    uploaded_by = serializers.SerializerMethodField()
    file_status = serializers.SerializerMethodField()
    cases_count = serializers.SerializerMethodField()
    tos_count = serializers.SerializerMethodField()

    class Meta:
        model = AllocationFileModel
        fields = [
            "id",
            "title",
            "product_assignment__process__title",
            "logo",
            "product_assignment__product__title",
            "cases_count",
            "tos_count",
            "upload_date",
            "uploaded_by",
            "file_status",
            "file_url",
            "latest_reupload_file_url",
            "latest_error_file_url",
        ]

    def get_uploaded_by(self, obj):
        if obj.core_generic_created_by and obj.core_generic_created_by.user:
            return obj.core_generic_created_by.user.username
        return None

    def get_file_status(self, obj):
        if obj.no_of_error_records > 0:
            return "ERROR"
        elif obj.expiry_date and obj.expiry_date < timezone.now():
            return "EXPIRED"
        return "VALID"

    def get_cases_count(self, obj):
        return getattr(obj, "cases_count", 0)

    def get_tos_count(self, obj):
        return getattr(obj, "tos_count", 0)
