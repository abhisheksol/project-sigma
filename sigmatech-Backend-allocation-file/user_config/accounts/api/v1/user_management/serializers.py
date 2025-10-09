from rest_framework import serializers
from typing import List, Optional
from user_config.accounts.api.v1.utils.handlers.user_management_create_user_handler import (
    UserManagementCreateUserHandler,
)
from django.db.models import Value
from django.db.models import CharField, Value
from django.db.models.functions import Concat
from user_config.accounts.api.v1.utils.handlers.user_management_update_user_handler import (
    UserManagementUpdateUserHandler,
)
from user_config.accounts.api.v1.utils.handlers.user_reassignment_handler import (
    UserManagementUserReAssignmentHandler,
)
from store.operations.case_management.models import CaseManagementCaseModel
from user_config.accounts.models import UserDetailModel
from user_config.accounts.api.v1.utils.user_table_field_utils import (
    get_user_instance_assigned_area_queryset,
    get_user_instance_assigned_city_queryset,
    get_user_instance_assigned_pincode_queryset,
    get_user_instance_assigned_region_queryset,
    get_user_instance_assigned_zone_queryset,
)
from user_config.user_auth.models import UserModel
from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
from store.configurations.region_config.models import (
    RegionConfigurationAreaModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
)
from django.db.models.query import QuerySet
from core_utils.utils.enums import CoreUtilsStatusEnum
from user_config.accounts.api.v1.user_management.handlerfo import FoAssignmentHandler 

class UserManagementUserCreateModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    region_id = serializers.UUIDField(required=False)
    zone_id = serializers.UUIDField(required=False)
    profile_picture = serializers.URLField(required=False, allow_blank=True)
    city_id = serializers.ListField(
        child=serializers.UUIDField(required=False), required=False, allow_empty=True
    )
    pincode_id = serializers.ListField(
        child=serializers.UUIDField(required=False), required=False, allow_empty=True
    )
    area_id = serializers.ListField(
        child=serializers.UUIDField(required=False), required=False, allow_empty=True
    )
    handler_class = UserManagementCreateUserHandler

    product_assignment_id = serializers.ListField(
        child=serializers.UUIDField(required=False),
        required=False,
        allow_empty=True,
    )

    class Meta:
        model = UserModel
        fields = [
            "username",
            "login_id",
            "email",
            "user_role",
            "phone_number",
            "profile_picture",
            "reports_to",
            "region_id",
            "zone_id",
            "city_id",
            "pincode_id",
            "area_id",
            "product_assignment_id",
        ]


class UserManagementUserUpdateModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):

    id = serializers.UUIDField(required=True)
    username = serializers.CharField(required=False)
    login_id = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    user_role = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    profile_picture = serializers.CharField(required=False)
    reports_to = serializers.CharField(required=False)
    region_id = serializers.UUIDField(required=False)
    zone_id = serializers.UUIDField(required=False)
    city_id = serializers.ListField(
        child=serializers.UUIDField(required=False), required=False, allow_empty=True
    )
    pincode_id = serializers.ListField(
        child=serializers.UUIDField(required=False), required=False, allow_empty=True
    )
    area_id = serializers.ListField(
        child=serializers.UUIDField(required=False), required=False, allow_empty=True
    )
    product_assignment_id = serializers.ListField(
        child=serializers.UUIDField(), required=False, allow_empty=True
    )
    product_unassignment_id = serializers.ListField(
        child=serializers.UUIDField(), required=False, allow_empty=True
    )

    handler_class = UserManagementUpdateUserHandler

    class Meta:
        model = UserModel
        fields = [
            "id",
            "username",
            "login_id",
            "email",
            "user_role",
            "phone_number",
            "profile_picture",
            "reports_to",
            "region_id",
            "zone_id",
            "city_id",
            "pincode_id",
            "area_id",
            "status",
            "product_assignment_id",
            "product_unassignment_id",
        ]


class UserManagementUserModelSerializerMethodFields:
    def get_assigned_region(self, obj: UserModel) -> Optional[str]:
        return ", ".join(
            get_user_instance_assigned_region_queryset(user_instance=obj).values_list(
                "title", flat=True
            )
        )

    def get_assigned_zone(self, obj: UserModel) -> Optional[str]:
        return ", ".join(
            get_user_instance_assigned_zone_queryset(user_instance=obj).values_list(
                "title", flat=True
            )
        )

    def get_assigned_city(self, obj: UserModel) -> List[str]:
        return get_user_instance_assigned_city_queryset(user_instance=obj).values_list(
            "city_name", flat=True
        )

    def get_assigned_pincode(self, obj: UserModel) -> List[str]:
        return get_user_instance_assigned_pincode_queryset(
            user_instance=obj
        ).values_list("pincode__pincode", flat=True)

    def get_assigned_area(self, obj: UserModel) -> List[str]:
        return get_user_instance_assigned_area_queryset(user_instance=obj).values_list(
            "title", flat=True
        )

    def get_has_reporting_users(self, obj: UserModel) -> bool:
        return obj.UserModel_reports_to.all().exists()


class UserManagementUserListModelSerializer(
    serializers.ModelSerializer, UserManagementUserModelSerializerMethodFields
):
    user_role__title = serializers.CharField(
        source="user_role.title", allow_blank=True, default=None
    )
    assigned_region = serializers.SerializerMethodField()
    assigned_zone = serializers.SerializerMethodField()
    assigned_pincode = serializers.SerializerMethodField()
    assigned_city = serializers.SerializerMethodField()
    assigned_area = serializers.SerializerMethodField()
    has_reporting_users = serializers.SerializerMethodField()
    product_assignment_name = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = [
            "id",
            "username",
            "user_role__title",
            "assigned_area",
            "assigned_region",
            "assigned_pincode",
            "assigned_city",
            "assigned_zone",
            "email",
            "status",
            "has_reporting_users",
            "product_assignment_name",
        ]

    def get_product_assignment_name(self, obj):
        # Extract the annotated "assignment" values from the prefetch
        return [a.assignment for a in getattr(obj, "product_assignment_name", [])]


class UserManagementUserDetailsModelSerializer(
    serializers.ModelSerializer, UserManagementUserModelSerializerMethodFields
):
    user_role = serializers.CharField(
        source="user_role.title", default=None, allow_blank=True
    )
    reports_to = serializers.CharField(
        source="reports_to.username", default=None, allow_blank=True
    )
    profile_picture = serializers.CharField(
        source="UserDetailModel_user.profile_picture", default=None, allow_blank=True
    )
    blood_group = serializers.CharField(
        source="UserDetailModel_user.blood_group", default=None, allow_blank=True
    )
    vehicle_number = serializers.CharField(
        source="UserDetailModel_user.vehicle_number", default=None, allow_blank=True
    )
    emergency_phone_number = serializers.CharField(
        source="UserDetailModel_user.emergency_phone_number",
        default=None,
        allow_blank=True,
    )
    emergency_contact_relation = serializers.CharField(
        source="UserDetailModel_user.emergency_contact_relation",
        default=None,
        allow_blank=True,
    )
    emergency_contact_relation_name = serializers.CharField(
        source="UserDetailModel_user.emergency_contact_relation_name",
        default=None,
        allow_blank=True,
    )
    product_assignment_name = serializers.SerializerMethodField()

    assigned_region = serializers.SerializerMethodField()
    assigned_zone = serializers.SerializerMethodField()
    assigned_pincode = serializers.SerializerMethodField()
    assigned_city = serializers.SerializerMethodField()
    assigned_area = serializers.SerializerMethodField()
    has_reporting_users = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = [
            "id",
            "username",
            "email",
            "login_id",
            "user_role",
            "reports_to",
            "phone_number",
            "status",
            "profile_picture",
            "blood_group",
            "vehicle_number",
            "emergency_phone_number",
            "emergency_contact_relation",
            "emergency_contact_relation_name",
            "assigned_area",
            "assigned_region",
            "assigned_pincode",
            "assigned_city",
            "assigned_zone",
            "has_reporting_users",
            "product_assignment_name",
        ]

    def get_product_assignment_name(self, obj):
        return list(
            obj.UserAssignedProdudctsModel_user.filter(
                status=CoreUtilsStatusEnum.ACTIVATED.value
            )
            .annotate(
                display_name=Concat(
                    "product_assignment__process__title",
                    Value("-"),
                    "product_assignment__product__title",
                    output_field=CharField(),
                )
            )
            .values_list("display_name", flat=True)
        )


class UserManagementUserUpdateDetailsModelSerializer(
    serializers.ModelSerializer, UserManagementUserModelSerializerMethodFields
):
    region_id = serializers.SerializerMethodField()
    zone_id = serializers.SerializerMethodField()
    city_id = serializers.SerializerMethodField()
    pincode_id = serializers.SerializerMethodField()
    area_id = serializers.SerializerMethodField()
    profile_picture = serializers.CharField(
        source="UserDetailModel_user.profile_picture", default=None, allow_blank=True
    )
    product_assignment_id = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = [
            "id",
            "username",
            "login_id",
            "user_role",
            "phone_number",
            "area_id",
            "region_id",
            "city_id",
            "reports_to",
            "pincode_id",
            "zone_id",
            "email",
            "status",
            "profile_picture",
            "product_assignment_id",
        ]

    def get_product_assignment_id(self, obj: UserModel):
        # return all product_assignment ids assigned to this user (only active ones if needed)
        return list(
            obj.UserAssignedProdudctsModel_user.filter(
                status=CoreUtilsStatusEnum.ACTIVATED.value
            ).values_list("product_assignment", flat=True)
        )

    def get_region_id(self, obj: UserModel):
        assigned_region: QuerySet[RegionConfigurationRegionModel] = (
            obj.UserDetailModel_user.assigned_region.all()
        )
        if assigned_region.exists():
            return assigned_region.last().pk
        return None

    def get_zone_id(self, obj: UserModel):
        assigned_zone: QuerySet[RegionConfigurationZoneModel] = (
            obj.UserDetailModel_user.assigned_zone.all()
        )
        if assigned_zone.exists():
            return assigned_zone.last().pk
        return None

    def get_city_id(self, obj: UserModel):
        assigned_city: QuerySet[RegionConfigurationCityModel] = (
            obj.UserDetailModel_user.assigned_city.all()
        )

        return assigned_city.values_list("pk", flat=True)

    def get_pincode_id(self, obj: UserModel):
        assigned_pincode: QuerySet[RegionConfigurationPincodeModel] = (
            obj.UserDetailModel_user.assigned_pincode.all()
        )

        return assigned_pincode.values_list("pk", flat=True)

    def get_area_id(self, obj: UserModel):
        assigned_area: QuerySet[RegionConfigurationAreaModel] = (
            obj.UserDetailModel_user.assigned_area.all()
        )

        return assigned_area.values_list("pk", flat=True)


class UserManagementAssignmentSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    reports_to_id = serializers.UUIDField()


class UserManagementUserReassignmentSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    assignment_data = UserManagementAssignmentSerializer(many=True, required=True)
    queryset = UserModel.objects.all()
    handler_class = UserManagementUserReAssignmentHandler




 
class EligibleFOListByCaseSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="user.username", read_only=True)
    user_id = serializers.UUIDField(source="user.id", read_only=True)
 
    class Meta:
        model = UserDetailModel
        fields = ["user_id", "label", "profile_picture"]


class FoAssignmentSerializer(CoreGenericSerializerMixin, serializers.Serializer):
    handler_class = FoAssignmentHandler

    case_id = serializers.UUIDField()
    fo_id = serializers.UUIDField()

    class Meta:
        model = CaseManagementCaseModel
        fields = ["case_id", "fo_id"]
