from rest_framework import serializers
from user_config.user_auth.models import UserModel
from store.operations.case_management.models import CaseManagementCaseModel
from store.operations.referal_files.models import FieldOfficerAssignment

from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin



class RefferralFileListingModelSerializer(serializers.ModelSerializer):
    pincode = serializers.SerializerMethodField(read_only=True)
    field_officer = serializers.SerializerMethodField(read_only=True)
    resolution_t = serializers.SerializerMethodField(read_only=True)
    assigned_cases = serializers.SerializerMethodField(read_only=True)
    upcoming_visit = serializers.SerializerMethodField(read_only=True)
    pos = serializers.SerializerMethodField(read_only=True)
    active_duty = serializers.SerializerMethodField(read_only=True)
    sub_areas = serializers.SerializerMethodField(read_only=True)
    actions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CaseManagementCaseModel
        fields = [
            "pincode",
            "field_officer",
            "resolution_t",
            "assigned_cases",
            "upcoming_visit",
            "pos",
            "active_duty",
            "sub_areas",
            "actions",
        ]

    # ✅ fetch real pincode from DB
    def get_pincode(self, obj):
        try:
            return obj.customer_office_pin_code.pincode.pincode
        except AttributeError:
            return None

    # ✅ static/default values (not from DB)
    def get_field_officer(self, obj):
        return "John Doe"

    def get_resolution_t(self, obj):
        return "In Progress"

    def get_assigned_cases(self, obj):
        return 12

    def get_upcoming_visit(self, obj):
        return "Tomorrow"

    def get_pos(self, obj):
        return 11

    def get_active_duty(self, obj):
        return True

    def get_sub_areas(self, obj):
        return ["Area A", "Area B"]

    def get_actions(self, obj):
        return ["Edit", "Delete"]














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
