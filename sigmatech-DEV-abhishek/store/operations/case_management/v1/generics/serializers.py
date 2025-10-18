from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
import datetime
from rest_framework import serializers
from store.operations.case_management.models import CaseManagementCaseModel
from store.operations.case_management.v1.generics.case_management_fields import (
    get_case_management_field_list,
)
from core_utils.utils.generics.views.generic_views import CoreGenericGetAPIView

CoreGenericGetAPIView


class CaseAllocationModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    allocation_file__product_assignment__process__title = serializers.CharField(
        read_only=True, source="allocation_file.product_assignment.process.title"
    )
    allocation_file__product_assignment__product__title = serializers.CharField(
        read_only=True, source="allocation_file.product_assignment.product.title"
    )
    # bucket_title = serializers.CharField(read_only=True)

    # region_title = serializers.CharField(read_only=True)
    channel_recommendation_title = serializers.CharField(read_only=True, default=None)
    latest_disposition_title = serializers.CharField(read_only=True, default=None)
    best_disposition_title = serializers.CharField(read_only=True, default=None)

    contact_score = serializers.SerializerMethodField()
    current_dpd = serializers.SerializerMethodField()
    residential_pin_code__pincode__pincode = serializers.IntegerField(
        source="residential_pin_code.pincode.pincode", read_only=True
    )
    customer_office_pin_code__pincode__pincode = serializers.IntegerField(
        source="customer_office_pin_code.pincode.pincode", read_only=True
    )

    default_manage_column_fields = [
        "id",
        "loan_account_number",
        "customer_name",
        "allocation_file__product_assignment__product__title",
        "bucket_name",
        "allocation_file__product_assignment__process__title",
        "current_dpd",
        "risk",
        "field_mapping_status",
        "channel_recommendation_title",
        "latest_disposition_title",
        "best_disposition_title",
        "contact_score",
        "total_loan_amount",
        "minimum_due_amount",
    ]

    class Meta:
        model = CaseManagementCaseModel
        fields = get_case_management_field_list(
            [
                "id",
                "residential_pin_code__pincode__pincode",
                "customer_office_pin_code__pincode__pincode",
                "customer_office_pin_code",
                # "loan_account_number",
                # "customer_name",
                "allocation_file__product_assignment__product__title",
                "bucket_name",
                "allocation_file__product_assignment__process__title",
                "current_dpd",
                "risk",
                "field_mapping_status",
                "channel_recommendation_title",
                "latest_disposition_title",
                "best_disposition_title",
                "contact_score",
            ]
        )

    def get_current_dpd(self, obj):
        if obj.due_date:
            today = datetime.date.today()
            diff_days = (today - obj.due_date).days
            return diff_days if diff_days > 0 else 0
        return None

    def get_contact_score(self, obj):
        # Use annotated field if present, else default 0
        return getattr(obj, "contact_score", 0)
