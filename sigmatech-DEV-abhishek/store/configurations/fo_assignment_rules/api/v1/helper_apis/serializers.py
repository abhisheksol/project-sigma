from rest_framework import serializers

from core_utils.utils.generics.serializers.generic_serializers import (
    CoreGenericHelperAPISerializerMethodField,
)
from store.configurations.region_config.models import RegionConfigurationPincodeModel
from user_config.user_auth.models import UserModel


class FOAssignementUSerHelperModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):
    zone_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    pincode_value = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = [
            "id",
            "username",
            "zone_name",
            "city_name",
            "pincode_value",
        ]

    def get_zone_name(self, obj):
        try:
            zone_title = obj.UserDetailModel_user.assigned_pincode.all().values_list(
                "city__zone__title", flat=True
            )

            return ", ".join(zone_title)
        except Exception as e:
            print(e)
            return None

    def get_city_name(self, obj):
        try:
            city_title = obj.UserDetailModel_user.assigned_pincode.all().values_list(
                "city__city_name", flat=True
            )
            return ", ".join(city_title)
        except AttributeError:
            return None

    def get_pincode_value(self, obj):
        try:
            pincode_title = obj.UserDetailModel_user.assigned_pincode.all().values_list(
                "pincode__pincode", flat=True
            )
            return ", ".join(pincode_title)
        except AttributeError:
            return None


class FOAssignementZoneHelperModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):
    zone = serializers.CharField(source="city.zone.title", read_only=True)
    pincode = serializers.CharField(source="pincode.pincode", read_only=True)
    city = serializers.CharField(source="city.city_name", read_only=True)
    id = serializers.UUIDField()
    subarea = serializers.SerializerMethodField()

    class Meta:
        model = RegionConfigurationPincodeModel
        fields = ["id", "zone", "pincode", "city", "subarea"]

    def get_subarea(self, obj):
        return obj.RegionConfigurationAreaModel_pincode.all().values_list(
            "title", flat=True
        )
