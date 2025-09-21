from rest_framework import serializers
from typing import List, Optional
from user_config.accounts.api.v1.utils.handlers.user_management_create_user_handler import (
    UserManagementCreateUserHandler,
)

from user_config.accounts.api.v1.utils.handlers.user_management_update_user_handler import (
    UserManagementUpdateUserHandler,
)
from user_config.accounts.api.v1.utils.handlers.user_reassignment_handler import (
    UserManagementUserReAssignmentHandler,
)
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
    print("update is running ....")
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
    unproduct_assignment_id = serializers.ListField(
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
            "unproduct_assignment_id"
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
    product_assignment_id = serializers.SerializerMethodField()

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
            "product_assignment_id",
        ]

    def get_product_assignment_id(self, obj):
        return list(
            obj.UserAssignedProdudctsModel_user.values_list(
                "product_assignment_id", flat=True
            )
        )

    # 🔥 Debugging override
    def to_representation(self, instance):
        data = super().to_representation(instance)
        print("\n=== 🔥🔥SERIALIZER DEBU🔥🔥 ===")
        for key, value in data.items():
            print(f"{key}: {value}")
        print("========================\n")
        return data


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
        ]


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
        ]

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
    assignment_data = UserManagementAssignmentSerializer(
        many=True, required=True)
    queryset = UserModel.objects.all()
    handler_class = UserManagementUserReAssignmentHandler
