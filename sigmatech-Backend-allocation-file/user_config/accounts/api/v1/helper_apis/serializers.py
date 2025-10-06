from rest_framework import serializers
from core_utils.utils.generics.serializers.generic_serializers import (
    CoreGenericHelperAPISerializerMethodField,
)
from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
from user_config.accounts.api.v1.utils.handlers.user_role_helper_list_handler import (
    UserRoleHelperListHanlder,
)
from user_config.user_auth.models import UserRoleModel
from django.contrib.auth import get_user_model
from store.configurations.region_config.models import (
    RegionConfigurationAreaModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
)
from store.configurations.loan_config.models import (
    LoanConfigurationsProductAssignmentModel,
)
from core_utils.utils.enums import CoreUtilsStatusEnum


class UserRoleHelperListSerializer(CoreGenericSerializerMixin, serializers.Serializer):
    results = serializers.JSONField(required=False)
    handler_class = UserRoleHelperListHanlder
    queryset = UserRoleModel.objects.all()


class UserReportsToHelperListModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):
    value = serializers.CharField(source="id", allow_blank=True, default="")
    label = serializers.CharField(source="username", allow_blank=True, default="")
    disabled = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            "value",
            "label",
            "disabled",
        ]


class UserManagementUserRegionHelperListModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):
    value = serializers.CharField(source="id", allow_blank=True, default="")
    label = serializers.CharField(source="title", allow_blank=True, default="")
    disabled = serializers.SerializerMethodField()

    class Meta:
        model = RegionConfigurationRegionModel
        fields = [
            "value",
            "label",
            "disabled",
        ]


class UserManagementUserZoneHelperListModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):
    value = serializers.CharField(source="id", allow_blank=True, default="")
    label = serializers.CharField(source="title", allow_blank=True, default="")
    disabled = serializers.SerializerMethodField()

    class Meta:
        model = RegionConfigurationZoneModel
        fields = [
            "value",
            "label",
            "disabled",
        ]


class UserManagementUserCityHelperListModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):
    value = serializers.CharField(source="id", allow_blank=True, default="")
    label = serializers.CharField(source="city_name", allow_blank=True, default="")
    disabled = serializers.SerializerMethodField()

    class Meta:
        model = RegionConfigurationCityModel
        fields = [
            "value",
            "label",
            "disabled",
        ]


class UserManagementUserPincodeHelperListModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):
    value = serializers.CharField(source="id", allow_blank=True, default="")
    label = serializers.CharField(
        source="pincode.pincode", allow_blank=True, default=""
    )
    disabled = serializers.SerializerMethodField()

    class Meta:
        model = RegionConfigurationPincodeModel
        fields = [
            "value",
            "label",
            "disabled",
        ]


class UserManagementUserAreaHelperListModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):
    value = serializers.CharField(source="id", allow_blank=True, default="")
    label = serializers.CharField(source="title", allow_blank=True, default="")
    disabled = serializers.SerializerMethodField()

    class Meta:
        model = RegionConfigurationAreaModel
        fields = [
            "value",
            "label",
            "disabled",
        ]


# !------------------------------ Abhishek ------------------------------


class ProductAssignmentHelperSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):
    value = serializers.UUIDField(source="pk", read_only=True)
    label = serializers.SerializerMethodField()
    disabled = serializers.SerializerMethodField()

    class Meta:
        model = LoanConfigurationsProductAssignmentModel
        fields = ["label", "value", "disabled", "status"]

    def get_label(self, obj):
        return f"{obj.process.title}-{obj.product.title}"

    def get_value(self, obj):
        return (
            obj.process.status == CoreUtilsStatusEnum.ACTIVATED.value
            and obj.product.status == CoreUtilsStatusEnum.ACTIVATED.value
            and obj.status == CoreUtilsStatusEnum.ACTIVATED.value
        )
