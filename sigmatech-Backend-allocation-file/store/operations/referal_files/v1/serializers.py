from rest_framework import serializers
from user_config.user_auth.models import UserModel
from store.operations.case_management.models import CaseManagementCaseModel
from store.operations.referal_files.models import FieldOfficerAssignment


class FieldOfficerListingSerializer(serializers.Serializer):
    field_officer = serializers.CharField()
    pin_codes = serializers.ListField()
    assigned_cases_count = serializers.IntegerField()
    

    def to_representation(self, obj):
        # Get all pincodes from cases
        pin_codes = list(
        CaseManagementCaseModel.objects.values_list(
        'customer_office_pin_code__pincode__pincode', 
        flat=True
        ).distinct()
)

        print(f"Pin codes: {pin_codes[0]}")

        # Get all users linked to those pincodes
        users = list(UserModel.objects.filter(
            UserDetailModel_user__assigned_pincode__pincode__pincode__in=pin_codes
        ).values_list('username', flat=True))

        # Get case count across pincodes
        cases_count = CaseManagementCaseModel.objects.filter(
           customer_office_pin_code__pincode__pincode__in=pin_codes
        ).count()

        print(f"Cases count: {cases_count}")

        return {
            "field_officer": obj.field_officer.username,
            "pin_codes": pin_codes,
            "assigned_cases_count": cases_count,
        }
