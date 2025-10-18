from django.utils import timezone
from rest_framework import serializers
from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
from store.operations.allocation_files.models import AllocationFileModel


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
        source="product_assignment.process.logo", default=None, allow_blank=True
    )

    core_generic_created_by__user__username = serializers.CharField(
        source="core_generic_created_by.user.username", allow_blank=True, default=None
    )
    file_status = serializers.SerializerMethodField()
    cases_count = serializers.IntegerField(read_only=True)
    tos_count = serializers.IntegerField(read_only=True)
    referred = serializers.IntegerField(read_only=True)

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
            "core_generic_created_at",
            "core_generic_created_by__user__username",
            "file_status",
            "file_url",
            "latest_reupload_file_url",
            "latest_error_file_url",
            "allocation_status",
            "referred",
        ]

    def get_file_status(self, obj):
        if obj.no_of_error_records > 0:
            return "ERROR"
        elif obj.expiry_date and obj.expiry_date < timezone.now():
            return "EXPIRED"
        return "VALID"


class AllocationFileDetailModelSerializer(serializers.ModelSerializer):
    cycle__id = serializers.CharField(source="cycle.pk", allow_blank=True, default=None)
    cycle__title = serializers.CharField(
        source="cycle.title", allow_blank=True, default=None
    )
    product__id = serializers.CharField(
        source="product_assignment.process.id", allow_blank=True, default=None
    )
    product__title = serializers.CharField(
        source="product_assignment.process.title", allow_blank=True, default=None
    )
    process__id = serializers.CharField(
        source="product_assignment.product.id", allow_blank=True, default=None
    )
    process__title = serializers.CharField(
        source="product_assignment.product.title", allow_blank=True, default=None
    )

    class Meta:
        model = AllocationFileModel
        fields = [
            "id",
            "title",
            "file_url",
            "initial_file_url",
            "latest_reupload_file_url",
            "latest_error_file_url",
            "no_of_total_records",
            "no_of_valid_records",
            "no_of_error_records",
            "no_of_duplicate_records",
            "expiry_date",
            "cycle__id",
            "cycle__title",
            "product__id",
            "product__title",
            "process__id",
            "process__title",
            "allocation_status",
        ]
