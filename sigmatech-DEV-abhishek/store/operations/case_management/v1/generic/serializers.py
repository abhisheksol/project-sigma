from store.operations.case_management.models import CaseManagementCaseModel
from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
from rest_framework import serializers


class CaseManagementListSerializer( CoreGenericSerializerMixin,
                                   serializers.ModelSerializer,
):
    # product = serializers.CharField(
    #     source='allocation_file.product_assignment.product.title',
    #     read_only=True
    # )
    # region = serializers.CharField(
    #     source='casemanagementcaseaddressmodel_assigned_case.first.region_config_city.zone.region.title',
    #     read_only=True
    # )
    # zone = serializers.CharField(
    #     source='casemanagementcaseaddressmodel_assigned_case.first.region_config_city.zone.title',
    #     read_only=True
    # )
    # pin_code = serializers.CharField(
    #     source='casemanagementcaseaddressmodel_assigned_case.first.pin_code.pincode.pincode',
    #     read_only=True
    # )

    class Meta:
        model = CaseManagementCaseModel
        fields = [
            'crn_number'
            
        ]


# class CaseManagementListSerializer(serializers.ModelSerializer):
#     # Computed fields from relationships
#     product = serializers.CharField(
#         source='allocation_file.product_assignment.product.title',
#         read_only=True
#     )
#     region = serializers.CharField(
#         source='casemanagementcaseaddressmodel_assigned_case.first.region_config_city.zone.region.title',
#         read_only=True
#     )
#     zone = serializers.CharField(
#         source='casemanagementcaseaddressmodel_assigned_case.first.region_config_city.zone.title',
#         read_only=True
#     )
#     pin_code = serializers.CharField(
#         source='casemanagementcaseaddressmodel_assigned_case.first.pin_code.pincode.pincode',
#         read_only=True
#     )

#     class Meta:
#         model = CaseManagementCaseModel
#         fields = [
#             'crn_number', 'customer_name', 'product',
#             'total_loan_amount', 'minimum_due_amount', 'current_dpd',
#             'region', 'zone', 'pin_code', 'substage', 'risk',
#             'channel_status', 'contact_mode', 'channel_recommendation',
#             'latest_disposition', 'best_disposition'
#         ]
